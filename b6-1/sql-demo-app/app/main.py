"""
위성 궤도/주파수 SQL 데모 백엔드 (FastAPI).

버튼 클릭 -> POST /sql-demo/api/run/{id} -> queries.py 화이트리스트에 있는
고정 SQL만 실행. 클라이언트가 임의의 SQL을 보낼 방법은 없다.

매 요청마다 sqlite3 in-memory DB를 새로 만들고 schema.sql + data.sql을 즉시
적용한 뒤 그 요청의 쿼리 하나만 실행하고 버린다. 그래서:
- 여러 방문자가 동시에 UPDATE/DELETE를 눌러도 서로 영향을 주지 않는다.
- 매 요청이 항상 원본 데이터 기준으로 재현 가능하다.
"""

import os
import sqlite3
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import auth
from app.auth_routes import router as auth_router
from app.queries import QUERIES, QUERIES_BY_ID

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_SQL = (BASE_DIR / "data" / "schema.sql").read_text(encoding="utf-8")
DATA_SQL = (BASE_DIR / "data" / "data.sql").read_text(encoding="utf-8")
STATIC_DIR = BASE_DIR / "app" / "static"

# 평가 기간에는 true로 두고 "실행 SQL"을 보여주다가, 평가가 끝나면 systemd 유닛의
# Environment=SHOW_SQL=false 로 바꾸고 서비스만 재시작하면 즉시 가려진다 (코드 재배포 불필요).
SHOW_SQL = os.environ.get("SHOW_SQL", "true").strip().lower() in ("1", "true", "yes")

# 운영 환경(HTTPS)에서는 항상 true. http://127.0.0.1로 로컬 테스트할 때만
# SESSION_HTTPS_ONLY=false로 잠깐 꺼서 Secure 쿠키 제약을 우회한다.
SESSION_HTTPS_ONLY = os.environ.get("SESSION_HTTPS_ONLY", "true").strip().lower() in (
    "1", "true", "yes",
)

app = FastAPI(title="위성 궤도/주파수 SQL 데모")
app.add_middleware(
    SessionMiddleware,
    secret_key=auth.get_or_create_session_secret(),
    https_only=SESSION_HTTPS_ONLY,
    same_site="lax",
)
app.include_router(auth_router)


def fresh_connection() -> sqlite3.Connection:
    """schema.sql + data.sql이 적용된 새 in-memory DB 커넥션을 만든다."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA_SQL)
    conn.executescript(DATA_SQL)
    return conn


@app.get("/sql-demo/api/queries")
def list_queries(username: str = Depends(auth.require_login)):
    return [
        {
            "id": q["id"],
            "category": q["category"],
            "description": q["description"],
            "kind": q["kind"],
            **({"sql": q["sql"].strip()} if SHOW_SQL else {}),
        }
        for q in QUERIES
    ]


@app.post("/sql-demo/api/run/{query_id}")
def run_query(query_id: str, username: str = Depends(auth.require_login)):
    query = QUERIES_BY_ID.get(query_id)
    if query is None:
        raise HTTPException(status_code=404, detail="존재하지 않는 쿼리 id입니다.")

    conn = fresh_connection()
    try:
        cur = conn.cursor()

        if query["kind"] == "error-demo":
            try:
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(query["sql"])
                conn.commit()
                return {"ok": True, "message": "예상과 달리 정상 삽입되었습니다 (버그 확인 필요)."}
            except sqlite3.IntegrityError as e:
                return {"ok": False, "error": str(e)}

        if query["kind"] == "mutate":
            cur.execute(query["sql"])
            rowcount = cur.rowcount
            conn.commit()
            return {
                "ok": True,
                "message": f"{rowcount}행 반영됨 "
                f"(이 데모는 요청마다 원본 데이터로 초기화되므로 실제로 저장되지는 않습니다.)",
            }

        # select / explain
        cur.execute(query["sql"])
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return {"ok": True, "columns": columns, "rows": rows}
    finally:
        conn.close()


app.mount("/sql-demo/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/sql-demo/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
