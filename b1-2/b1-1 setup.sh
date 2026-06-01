#!/bin/bash
# =============================================================
# setup.sh - B1-1 환경 자동 복구 스크립트
# 포맷 후 실행하면 B1-1 전체 환경이 자동으로 구성됩니다.
#
# 실행 방법:
#   chmod +x setup.sh
#   sudo bash setup.sh
#
# 소요 시간: 약 2~3분
# =============================================================

set -e  # 오류 발생 시 즉시 중단

# ── 색상 출력 설정 ────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
info() { echo -e "${YELLOW}[INFO]${NC} $1"; }
err()  { echo -e "${RED}[ERR]${NC}  $1"; exit 1; }

# ── root 권한 확인 ────────────────────────────────────────────
if [ "$(id -u)" -ne 0 ]; then
    err "이 스크립트는 sudo로 실행해야 합니다: sudo bash setup.sh"
fi

echo ""
echo "======================================================"
echo "  B1-1 환경 자동 복구 스크립트"
echo "======================================================"
echo ""

# ──────────────────────────────────────────────────────────────
# STEP 1: 필수 패키지 설치
# ──────────────────────────────────────────────────────────────
info "[1/6] 필수 패키지 설치 중..."

apt-get update -qq
apt-get install -y -qq acl ufw net-tools cron

ok "패키지 설치 완료 (acl, ufw, net-tools, cron)"

# ──────────────────────────────────────────────────────────────
# STEP 2: 그룹 및 계정 생성
# ──────────────────────────────────────────────────────────────
info "[2/6] 그룹 및 계정 생성 중..."

# 그룹 생성 (이미 있으면 건너뜀)
groupadd agent-common 2>/dev/null && ok "그룹 agent-common 생성" || info "그룹 agent-common 이미 존재"
groupadd agent-core   2>/dev/null && ok "그룹 agent-core 생성"   || info "그룹 agent-core 이미 존재"

# 계정 생성 (이미 있으면 건너뜀)
id agent-admin &>/dev/null || (useradd -m -s /bin/bash agent-admin && ok "계정 agent-admin 생성")
id agent-dev   &>/dev/null || (useradd -m -s /bin/bash agent-dev   && ok "계정 agent-dev 생성")
id agent-test  &>/dev/null || (useradd -m -s /bin/bash agent-test  && ok "계정 agent-test 생성")

# 비밀번호 설정
echo "agent-admin:Admin1234" | chpasswd
echo "agent-dev:Dev1234"     | chpasswd
echo "agent-test:Test1234"   | chpasswd
ok "비밀번호 설정 완료 (admin:Admin1234 / dev:Dev1234 / test:Test1234)"

# 그룹 배정
usermod -aG agent-common agent-admin
usermod -aG agent-common agent-dev
usermod -aG agent-common agent-test
usermod -aG agent-core   agent-admin
usermod -aG agent-core   agent-dev
usermod -aG sudo         agent-admin
ok "그룹 배정 완료"

# ──────────────────────────────────────────────────────────────
# STEP 3: 디렉토리 구조 생성 및 권한 설정
# ──────────────────────────────────────────────────────────────
info "[3/6] 디렉토리 구조 및 권한 설정 중..."

# 디렉토리 생성
mkdir -p /home/agent-admin/agent-app/upload_files
mkdir -p /home/agent-admin/agent-app/api_keys
mkdir -p /home/agent-admin/agent-app/bin
mkdir -p /var/log/agent-app

# 소유자 설정
chown -R agent-admin:agent-admin /home/agent-admin/agent-app
chown agent-admin:agent-common   /home/agent-admin/agent-app/upload_files
chown agent-admin:agent-core     /home/agent-admin/agent-app/api_keys
chown agent-admin:agent-core     /var/log/agent-app

# 권한 설정
chmod 2775 /home/agent-admin/agent-app/upload_files
chmod 750  /home/agent-admin/agent-app/api_keys
chmod 770  /var/log/agent-app

# ACL 설정
setfacl -m  g:agent-common:rwx /home/agent-admin/agent-app/upload_files
setfacl -d -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files

setfacl -m  g:agent-core:rwx /home/agent-admin/agent-app/api_keys
setfacl -d -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys

setfacl -m  g:agent-core:rwx /var/log/agent-app
setfacl -d -m g:agent-core:rwx /var/log/agent-app

ok "디렉토리 구조 및 ACL 권한 설정 완료"

# ──────────────────────────────────────────────────────────────
# STEP 4: 앱 파일 복사 및 키 파일 생성
# ──────────────────────────────────────────────────────────────
info "[4/6] 앱 파일 및 키 파일 설정 중..."

# 앱 바이너리 복사 (Mac 마운트 경로에서 자동 탐색)
APP_SRC=""
for path in \
    "/mac/Users/cspag5955/OrbStack/AI-SW-ubuntu24/home/cspag5955/AI-SW-Basic/b1-1/실행파일/agent-app-linux-arm64" \
    "/mac/Users/cspag5955/OrbStack/AI-SW-ubuntu24/home/cspag5955/AI-SW-Basic/b1-1/실행파일/agent-app-linux-x86" \
    "/tmp/agent-app-linux-arm64" \
    "/tmp/agent-app-linux-x86"; do
    if [ -f "$path" ]; then
        APP_SRC="$path"
        break
    fi
done

if [ -n "$APP_SRC" ]; then
    cp "$APP_SRC" /home/agent-admin/agent-app/agent-app
    chmod +x /home/agent-admin/agent-app/agent-app
    chown agent-admin:agent-admin /home/agent-admin/agent-app/agent-app
    ok "앱 바이너리 복사 완료: $APP_SRC"
else
    info "앱 바이너리를 찾지 못했습니다. 수동으로 복사하세요:"
    info "  cp /tmp/agent-app-linux-x86 /home/agent-admin/agent-app/agent-app"
    info "  chmod +x /home/agent-admin/agent-app/agent-app"
fi

# 키 파일 생성
printf "agent_api_key_test\n" > /home/agent-admin/agent-app/api_keys/t_secret.key
chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key
chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/t_secret.key
ok "키 파일 생성 완료 (t_secret.key)"

# B1-2용 secret.key도 함께 생성
printf "agent_api_key_test\n" > /home/agent-admin/agent-app/api_keys/secret.key
chmod 600 /home/agent-admin/agent-app/api_keys/secret.key
chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/secret.key
ok "키 파일 생성 완료 (secret.key - B1-2용)"

# ──────────────────────────────────────────────────────────────
# STEP 5: 환경변수 설정 (.bashrc)
# ──────────────────────────────────────────────────────────────
info "[5/6] 환경변수 설정 중..."

# 기존 Agent 환경변수 블록 제거 후 재등록 (중복 방지)
BASHRC="/home/agent-admin/.bashrc"

# 기존 블록 제거
sed -i '/# ===== Agent 환경변수 =====/,/^$/d' "$BASHRC" 2>/dev/null || true
sed -i '/# ===== B1-2 추가 환경변수 =====/,/^$/d' "$BASHRC" 2>/dev/null || true

# 환경변수 추가
cat >> "$BASHRC" << 'EOF'

# ===== Agent 환경변수 (B1-1) =====
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app

# ===== B1-2 추가 환경변수 =====
export MEMORY_LIMIT=256
export CPU_MAX_OCCUPY=50
export MULTI_THREAD_ENABLE=true
EOF

chown agent-admin:agent-admin "$BASHRC"
ok "환경변수 설정 완료 (.bashrc)"

# ──────────────────────────────────────────────────────────────
# STEP 6: monitor.sh 설치 및 crontab 등록
# ──────────────────────────────────────────────────────────────
info "[6/6] monitor.sh 설치 및 crontab 등록 중..."

# monitor.sh 작성
cat > /home/agent-admin/agent-app/bin/monitor.sh << 'MONITOR_EOF'
#!/bin/bash
# monitor.sh - 시스템 관제 자동화 스크립트

APP_PROCESS="agent-app"
APP_PORT=15034
LOG_FILE="/var/log/agent-app/monitor.log"
MAX_LOG_SIZE=$((10 * 1024 * 1024))
MAX_LOG_FILES=10
CPU_THRESHOLD=20
MEM_THRESHOLD=10
DISK_THRESHOLD=80

rotate_log() {
    [ ! -f "$LOG_FILE" ] && return
    local size
    size=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$size" -ge "$MAX_LOG_SIZE" ]; then
        for i in $(seq $((MAX_LOG_FILES - 1)) -1 1); do
            [ -f "${LOG_FILE}.$i" ] && mv "${LOG_FILE}.$i" "${LOG_FILE}.$((i + 1))"
        done
        mv "$LOG_FILE" "${LOG_FILE}.1"
        touch "$LOG_FILE"
    fi
}

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""
echo "[HEALTH CHECK]"

PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    exit 1
else
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
fi

PORT_STATUS=$(ss -tulnp 2>/dev/null | grep ":${APP_PORT} ")
if [ -z "$PORT_STATUS" ]; then
    echo "Checking port $APP_PORT... [FAIL] Port not listening!"
    exit 1
else
    echo "Checking port $APP_PORT... [OK]"
fi

echo ""
echo "[FIREWALL CHECK]"
if systemctl is-active --quiet ufw 2>/dev/null; then
    echo "Firewall (UFW)... [OK] Active"
else
    echo "[WARNING] Firewall (UFW) is not active!"
fi
echo ""

echo "[RESOURCE MONITORING]"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")

MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
MEM_USED=$(free  | grep Mem | awk '{print $3}')
if [ "${MEM_TOTAL:-0}" -gt 0 ]; then
    MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEM_USAGE="0.0"
fi

DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""

CPU_INT=$(echo "$CPU_USAGE" | cut -d'.' -f1)
[ "${CPU_INT:-0}"    -gt "$CPU_THRESHOLD"  ] && echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
MEM_INT=$(echo "$MEM_USAGE" | cut -d'.' -f1)
[ "${MEM_INT:-0}"    -gt "$MEM_THRESHOLD"  ] && echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
[ "${DISK_USAGE:-0}" -gt "$DISK_THRESHOLD" ] && echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"

echo ""
echo "===================================="

LOG_DIR=$(dirname "$LOG_FILE")
[ ! -d "$LOG_DIR" ] && mkdir -p "$LOG_DIR" 2>/dev/null
rotate_log
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"
echo "[INFO] Log appended: $LOG_FILE"
MONITOR_EOF

# monitor.sh 소유자/권한 설정
chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
ok "monitor.sh 설치 완료"

# cron 서비스 시작
systemctl enable cron 2>/dev/null || systemctl enable crond 2>/dev/null || true
systemctl start  cron 2>/dev/null || systemctl start  crond 2>/dev/null || true

# agent-admin crontab 등록
CRON_JOB="* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1"
(crontab -u agent-admin -l 2>/dev/null | grep -v "monitor.sh"; echo "$CRON_JOB") | crontab -u agent-admin -
ok "crontab 등록 완료 (매분 자동 실행)"

# sudo NOPASSWD 설정 (cron에서 sudo 없이 ufw 상태 확인)
SUDOERS_LINE="agent-admin ALL=(ALL) NOPASSWD: /usr/sbin/ufw status, /usr/sbin/ufw *"
if ! grep -q "agent-admin" /etc/sudoers 2>/dev/null; then
    echo "$SUDOERS_LINE" >> /etc/sudoers
    ok "sudoers NOPASSWD 설정 완료"
fi

# ──────────────────────────────────────────────────────────────
# 완료 요약
# ──────────────────────────────────────────────────────────────
echo ""
echo "======================================================"
echo "  환경 복구 완료!"
echo "======================================================"
echo ""
echo "  계정 및 비밀번호:"
echo "    agent-admin / Admin1234  (sudo 권한)"
echo "    agent-dev   / Dev1234"
echo "    agent-test  / Test1234"
echo ""
echo "  디렉토리:"
echo "    앱 홈    : /home/agent-admin/agent-app/"
echo "    로그     : /var/log/agent-app/"
echo ""
echo "  환경변수 (agent-admin 계정 로그인 시 자동 적용):"
echo "    AGENT_HOME=/home/agent-admin/agent-app"
echo "    AGENT_PORT=15034"
echo "    MEMORY_LIMIT=256"
echo "    CPU_MAX_OCCUPY=50"
echo "    MULTI_THREAD_ENABLE=true"
echo ""
echo "  monitor.sh: 매분 자동 실행 (crontab 등록됨)"
echo ""
echo "  다음 단계:"
echo "    1. SSH 보안 설정 (포트 20022, Root 차단)"
echo "    2. 방화벽 설정 (UFW 20022, 15034 허용)"
echo "    3. su - agent-admin 후 앱 실행 확인"
echo ""
echo "  앱 실행:"
echo "    su - agent-admin"
echo "    /home/agent-admin/agent-app/agent-app"
echo ""
