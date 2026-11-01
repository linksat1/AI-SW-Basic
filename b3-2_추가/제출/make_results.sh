#!/usr/bin/env bash
# 제출/results/*.txt 증빙을 다시 만든다.
# 사용: bash 제출/make_results.sh [python 경로]   (b3-2_추가 폴더에서 실행)
# 04번(실제 API 인증 실패)은 anthropic 패키지와 네트워크가 필요하다.
set -u
PY="${1:-python3}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$HERE/제출/results"
DEMO="$(mktemp -d)"
mkdir -p "$OUT"
unset AI_API_KEY ANTHROPIC_API_KEY

run() {  # run <결과파일> <설명> <명령...>
  local file="$OUT/$1"; shift
  local title="$1"; shift
  {
    echo "# $title"
    echo "\$ $*"
    echo
    "$@" 2>&1 < /dev/null
    local rc=$?
    echo
    echo "(exit code: $rc)"
  } > "$file"
}

cd "$DEMO"
git init -q && git config user.email demo@example.com && git config user.name demo
cat > session.py <<'EOF'
def create_session(user):
    return {"user": user}
EOF
git add . && git commit -qm "Add session module"

run 01_변경없음.txt "변경 사항이 없을 때" "$PY" "$HERE/main.py" describe --mock

cat > session.py <<'EOF'
class SessionError(Exception):
    """세션 생성/검증 실패."""


def create_session(user):
    if not user or not user.strip():
        raise SessionError("empty user")
    return {"user": user.strip(), "active": True}


def validate_session(session):
    if not session or not session.get("active"):
        raise SessionError("inactive session")
    return True
EOF
cat > config.py <<'EOF'
API_KEY = "sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123"
ADMIN_EMAIL = "admin@example.com"
SUPPORT_PHONE = "010-1234-5678"
EOF
for i in $(seq 1 12); do printf 'def handler_%s():\n    return %s\n' "$i" "$i" > "handler_$i.py"; done

INTENT="로그인 세션 처리를 수정했고, 세션 검증과 예외 처리를 보완했다."
run 02_mock_전체흐름.txt "API 없이 전체 흐름 확인 (--mock, --intent)" \
  "$PY" "$HERE/main.py" describe --mock --intent "$INTENT"
run 03_API키_미설정.txt "API Key 환경변수 미설정" "$PY" "$HERE/main.py" describe --intent "$INTENT"
run 04_API_인증실패.txt "잘못된 API Key로 실제 API 호출 (401 원인 출력)" \
  env AI_API_KEY=sk-ant-invalid-key-for-demo "$PY" "$HERE/main.py" describe --intent "$INTENT"
mkdir -p sub
run 05_실행위치_오류.txt "저장소 루트가 아닌 곳 / git 저장소가 아닌 곳에서 실행" \
  bash -c "cd sub && '$PY' '$HERE/main.py' describe --mock; echo '(exit code: '\$?')'; cd /; '$PY' '$HERE/main.py' describe --mock"

{
  echo "# safe-mode OFF/ON 비교 (--dry-run: AI로 보낼 프롬프트만 출력, API 미호출)"
  echo "정책: 기본 최대 10개 파일, 최대 200줄 / API Key·토큰·비밀번호·이메일·전화번호 마스킹"
  echo
  echo "## OFF: \$ main.py describe --dry-run --intent ..."
  "$PY" "$HERE/main.py" describe --dry-run --intent "$INTENT" 2>&1 | grep -E '^\[|^\+(API_KEY|ADMIN|SUPPORT)|^## 변경 파일|^diff --git' | head -40
  echo
  echo "## ON: \$ main.py describe --dry-run --safe-mode --intent ..."
  "$PY" "$HERE/main.py" describe --dry-run --safe-mode --intent "$INTENT" 2>&1 | grep -E '^\[|^\+(API_KEY|ADMIN|SUPPORT)|^## 변경 파일|^diff --git|^\.\.\. \(safe' | head -40
  echo
  echo "## ON + 정책 조정: \$ main.py describe --dry-run --safe-mode --max-files 3 --max-diff-lines 40 --mask-pattern 'handler_[0-9]+'"
  "$PY" "$HERE/main.py" describe --dry-run --safe-mode --max-files 3 --max-diff-lines 40 \
    --mask-pattern 'handler_[0-9]+' --intent "$INTENT" 2>&1 | grep -E '^\[|^diff --git|^\.\.\. \(safe|MASKED_CUSTOM' | head -20
} > "$OUT/06_safe-mode_OFF_ON_비교.txt"

{
  echo "# 컨벤션 적용 전/후 비교"
  echo
  echo "## 적용 전 (내장 기본 컨벤션): \$ main.py describe --mock --intent ..."
  "$PY" "$HERE/main.py" describe --mock --intent "Mini Git 세션 검증 보완" 2>&1 | sed -n '/컨벤션/p;/Description Title/,/Description Body/p;/Validation/,$p'
  echo
  echo "## 적용 후: \$ main.py describe --mock --convention conventions/ai-sw-basic.json --intent ..."
  "$PY" "$HERE/main.py" describe --mock --convention "$HERE/conventions/ai-sw-basic.json" \
    --intent "Mini Git 세션 검증 보완" 2>&1 | sed -n '/컨벤션/p;/Description Title/,/Description Body/p;/Validation/,$p'
  echo
  echo "## AI에게 전달되는 작성 규칙 차이 (--dry-run 프롬프트의 '## 작성 규칙' 구간)"
  echo "### 적용 전"
  "$PY" "$HERE/main.py" describe --dry-run --intent x 2>&1 | sed -n '/^## 작성 규칙/,/^## 출력 형식/p' | sed '$d'
  echo "### 적용 후"
  "$PY" "$HERE/main.py" describe --dry-run --intent x --convention "$HERE/conventions/ai-sw-basic.json" 2>&1 \
    | sed -n '/^## 작성 규칙/,/^## 출력 형식/p' | sed '$d'
} > "$OUT/07_컨벤션_적용전후_비교.txt"

run 08_검증실패_재생성_후처리.txt "형식 오류 응답 -> 1회 재생성 -> 후처리 보정 (AI 응답은 시뮬레이션)" \
  "$PY" "$HERE/제출/simulate_invalid_response.py" "$DEMO"

cd "$HERE"
run 09_자동검증.txt "자동 테스트" "$PY" -B -m unittest discover -s tests -v
run 10_옵션_도움말.txt "CLI 옵션 (model / max-tokens / effort / temperature / safe-mode)" \
  "$PY" "$HERE/main.py" describe --help

# 제출용으로 로컬 절대경로를 짧은 표기로 바꾼다.
for f in "$OUT"/*.txt; do
  PY_P="$PY" HERE_P="$HERE" DEMO_P="$DEMO" perl -i -pe '
    s/\Q$ENV{PY_P}\E/python3/g; s/\Q$ENV{HERE_P}\E/./g;
    s/(\/private)?\Q$ENV{DEMO_P}\E/<demo-repo>/g' "$f"
done
rm -rf "$DEMO"
echo "결과 저장: $OUT"
