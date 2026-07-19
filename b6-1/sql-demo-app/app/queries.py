"""
위성 궤도/주파수 SQL 데모의 쿼리 화이트리스트.

여기 정의된 SQL만 서버에서 실행된다 — 클라이언트는 이 목록의 id만 지정할 수 있고,
자유 텍스트 SQL을 보낼 방법은 없다 (main.py의 /api/run/{id} 참고).
"""

# kind: "select" | "explain" | "mutate" | "error-demo"
QUERIES = [
    # ── 기본조회 (4) ──────────────────────────────────────────────
    {
        "id": "01",
        "category": "기본조회",
        "description": "최근 접수된 정지궤도(GSO) 위성망 신고 5건을 접수일 내림차순으로 확인한다.",
        "kind": "select",
        "sql": """
            SELECT ntc_id, adm, d_rcv
            FROM notice
            WHERE ntc_type = 'G'
            ORDER BY d_rcv DESC
            LIMIT 5;
        """,
    },
    {
        "id": "02",
        "category": "기본조회",
        "description": "한국(KOR)이 신고한 위성망 목록을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT ntc_id, adm, ntc_type, d_rcv
            FROM notice
            WHERE adm = 'KOR';
        """,
    },
    {
        "id": "03",
        "category": "기본조회",
        "description": "동경 90도 이상에 위치한 정지궤도 위성의 궤도 위치를 경도 오름차순으로 확인한다.",
        "kind": "select",
        "sql": """
            SELECT sat_name, long_nom
            FROM geo
            WHERE long_nom >= 90
            ORDER BY long_nom ASC;
        """,
    },
    {
        "id": "04",
        "category": "기본조회",
        "description": "Ku 대역(10,000~13,000MHz)에 속하는 주파수 대역을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT ntc_id, emi_rcp, freq_min, freq_max
            FROM freq
            WHERE freq_min >= 10000 AND freq_max <= 13000
            ORDER BY freq_min;
        """,
    },
    # ── 조인 (4: INNER 3 + LEFT 1) ───────────────────────────────
    {
        "id": "05",
        "category": "조인",
        "description": "[INNER 1] 위성망 이름과 신고국, 궤도 경도를 함께 확인한다.",
        "kind": "select",
        "sql": """
            SELECT n.ntc_id, n.adm, g.sat_name, g.long_nom
            FROM notice n
            INNER JOIN geo g ON n.ntc_id = g.ntc_id
            ORDER BY g.long_nom;
        """,
    },
    {
        "id": "06",
        "category": "조인",
        "description": "[INNER 2] 비정지궤도 신고의 신고국과 궤도면별 위성 수/경사각을 함께 확인한다.",
        "kind": "select",
        "sql": """
            SELECT n.ntc_id, n.adm, o.orb_id, o.nbr_sat_pl, o.inclin_ang
            FROM notice n
            INNER JOIN orbit o ON n.ntc_id = o.ntc_id
            ORDER BY n.ntc_id, o.orb_id;
        """,
    },
    {
        "id": "07",
        "category": "조인",
        "description": "[INNER 3] 한국(KOR)이 신고한 위성망의 주파수 대역을 위성 이름과 함께 확인한다.",
        "kind": "select",
        "sql": """
            SELECT n.adm, g.sat_name, f.emi_rcp, f.freq_min, f.freq_max
            FROM notice n
            INNER JOIN geo g ON n.ntc_id = g.ntc_id
            INNER JOIN freq f ON n.ntc_id = f.ntc_id
            WHERE n.adm = 'KOR';
        """,
    },
    {
        "id": "08",
        "category": "조인",
        "description": "[LEFT 1] 모든 신고에 대해 정지궤도 위치 정보 유무를 확인한다. (비정지궤도 신고는 NULL로 남음)",
        "kind": "select",
        "sql": """
            SELECT n.ntc_id, n.adm, n.ntc_type, g.sat_name, g.long_nom
            FROM notice n
            LEFT JOIN geo g ON n.ntc_id = g.ntc_id
            ORDER BY n.ntc_id;
        """,
    },
    # ── 집계 (3) ─────────────────────────────────────────────────
    {
        "id": "09",
        "category": "집계",
        "description": "신고국(adm)별 위성망 신고 건수를 확인한다. (COUNT + GROUP BY)",
        "kind": "select",
        "sql": """
            SELECT adm, COUNT(*) AS 신고건수
            FROM notice
            GROUP BY adm
            ORDER BY 신고건수 DESC;
        """,
    },
    {
        "id": "10",
        "category": "집계",
        "description": "신고별 주파수 대역 개수와 평균 대역폭을 확인한다. (COUNT, AVG + GROUP BY)",
        "kind": "select",
        "sql": """
            SELECT ntc_id, COUNT(*) AS 대역수, ROUND(AVG(bdwdth), 1) AS 평균대역폭_kHz
            FROM freq
            GROUP BY ntc_id
            ORDER BY 대역수 DESC;
        """,
    },
    {
        "id": "11",
        "category": "집계",
        "description": "비정지궤도 신고별 전체 궤도면의 위성 수 합계를 확인한다. (SUM + GROUP BY)",
        "kind": "select",
        "sql": """
            SELECT ntc_id, SUM(nbr_sat_pl) AS 총위성수
            FROM orbit
            GROUP BY ntc_id;
        """,
    },
    # ── 서브쿼리 (1) ─────────────────────────────────────────────
    {
        "id": "12",
        "category": "서브쿼리",
        "description": "전체 평균 대역폭보다 넓은 주파수 대역을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT ntc_id, emi_rcp, freq_min, freq_max, bdwdth
            FROM freq
            WHERE bdwdth > (SELECT AVG(bdwdth) FROM freq)
            ORDER BY bdwdth DESC;
        """,
    },
    # ── 수정/삭제 (2) ────────────────────────────────────────────
    {
        "id": "13",
        "category": "수정/삭제",
        "description": "[UPDATE] 아직 심사 중(st_cur=20)인 베트남(VTN) 신고를 처리 완료 상태(50)로 승인 처리한다.",
        "kind": "mutate",
        "sql": """
            UPDATE notice
            SET st_cur = 50
            WHERE adm = 'VTN' AND st_cur = 20;
        """,
    },
    {
        "id": "14",
        "category": "수정/삭제",
        "description": "[DELETE] 대역폭이 1,000,000kHz(=1GHz, Ka 대역 초광대역 피더링크)를 넘는 주파수 대역을 정리한다.",
        "kind": "mutate",
        "sql": """
            DELETE FROM freq
            WHERE bdwdth >= 1000000;
        """,
    },
    # ── 인덱스 (1) ───────────────────────────────────────────────
    {
        "id": "15",
        "category": "인덱스",
        "description": "freq.ntc_id로 notice와 JOIN하는 경우가 많아 idx_freq_ntc_id 인덱스를 적용했다. "
        "아래 쿼리로 인덱스가 실제로 사용되는지 실행 계획을 확인한다.",
        "kind": "explain",
        "sql": """
            EXPLAIN QUERY PLAN
            SELECT n.adm, f.freq_min, f.freq_max
            FROM notice n
            INNER JOIN freq f ON n.ntc_id = f.ntc_id
            WHERE f.ntc_id = 125520109;
        """,
    },
    # ── 보너스 1: JOIN vs 서브쿼리 비교 ──────────────────────────
    {
        "id": "bonus1-join",
        "category": "보너스1-JOIN vs 서브쿼리",
        "description": "[JOIN 버전] 정지궤도(GSO)로 등록된 위성망 신고만 조회한다.",
        "kind": "select",
        "sql": """
            SELECT DISTINCT n.ntc_id, n.adm, n.d_rcv
            FROM notice n
            INNER JOIN geo g ON n.ntc_id = g.ntc_id
            ORDER BY n.ntc_id;
        """,
    },
    {
        "id": "bonus1-subquery",
        "category": "보너스1-JOIN vs 서브쿼리",
        "description": "[서브쿼리 버전] 동일한 요구사항(GSO 신고만 조회)을 IN 서브쿼리로 푼다. 결과는 JOIN 버전과 동일하다.",
        "kind": "select",
        "sql": """
            SELECT n.ntc_id, n.adm, n.d_rcv
            FROM notice n
            WHERE n.ntc_id IN (SELECT ntc_id FROM geo)
            ORDER BY n.ntc_id;
        """,
    },
    # ── 보너스 2: 정합성 깨뜨려보기 ───────────────────────────────
    {
        "id": "bonus2-fk-violation",
        "category": "보너스2-정합성 깨뜨려보기",
        "description": "존재하지 않는 부모 ntc_id(999999999)로 geo에 INSERT를 시도한다. "
        "FOREIGN KEY 제약이 실제로 막아주는지 확인한다.",
        "kind": "error-demo",
        "sql": """
            INSERT INTO geo (ntc_id, sat_name, long_nom)
            VALUES (999999999, 'GHOST-SAT', 100);
        """,
    },
    # ── 보너스 3: 미니 리포트 (핵심 지표 3개) ────────────────────
    {
        "id": "bonus3-adm-share",
        "category": "보너스3-미니 리포트",
        "description": "[지표 1] 신고국(adm)별 신고 건수 및 비중(%)을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT adm, COUNT(*) AS 건수,
                   ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM notice), 1) AS 비중_퍼센트
            FROM notice
            GROUP BY adm
            ORDER BY 건수 DESC;
        """,
    },
    {
        "id": "bonus3-orbit-type",
        "category": "보너스3-미니 리포트",
        "description": "[지표 2] 정지궤도(GSO) vs 비정지궤도(NGSO) 신고 비율을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT ntc_type, COUNT(*) AS 건수,
                   ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM notice), 1) AS 비중_퍼센트
            FROM notice
            GROUP BY ntc_type;
        """,
    },
    {
        "id": "bonus3-band",
        "category": "보너스3-미니 리포트",
        "description": "[지표 3] 주파수 대역(L/S·C·Ku·Ka) 구분별 신고 건수 및 평균 대역폭을 확인한다.",
        "kind": "select",
        "sql": """
            SELECT
              CASE
                WHEN freq_min < 1000  THEN '1.L/S 이하'
                WHEN freq_min < 8000  THEN '2.C 대역'
                WHEN freq_min < 18000 THEN '3.Ku 대역'
                ELSE '4.Ka 대역 이상'
              END AS 대역구분,
              COUNT(*) AS 건수,
              ROUND(AVG(bdwdth), 0) AS 평균대역폭_kHz
            FROM freq
            GROUP BY 대역구분
            ORDER BY 대역구분;
        """,
    },
]

QUERIES_BY_ID = {q["id"]: q for q in QUERIES}
