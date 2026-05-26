#!/bin/bash
# =============================================================
# monitor.sh - 시스템 관제 자동화 스크립트
# 소유자: agent-dev  그룹: agent-core  권한: 750
# 실행자: agent-admin (agent-core 그룹 소속)
# VM 경로: /home/agent-admin/agent-app/bin/monitor.sh
# =============================================================

# ---- 설정값 ----
APP_PROCESS="agent-app-linux-arm64"        # 감시할 프로세스 이름
APP_PORT=15034                              # 감시할 포트 번호
LOG_FILE="/var/log/agent-app/monitor.log"  # 로그 파일 경로
MAX_LOG_SIZE=$((10 * 1024 * 1024))         # 최대 로그 크기: 10MB
MAX_LOG_FILES=10                            # 최대 로그 파일 개수

# ---- 임계값 ----
CPU_THRESHOLD=20
MEM_THRESHOLD=10
DISK_THRESHOLD=80

# ---- 로그 로테이션 함수 ----
rotate_log() {
    if [ ! -f "$LOG_FILE" ]; then
        return
    fi
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

# ---- 현재 시각 ----
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""

# =============================================================
# [1] HEALTH CHECK - 프로세스 및 포트 확인
# =============================================================
echo "[HEALTH CHECK]"

# 프로세스 확인 (비정상 시 exit 1)
PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    exit 1
else
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
fi

# 포트 확인 (비정상 시 exit 1)
PORT_STATUS=$(ss -tulnp 2>/dev/null | grep ":${APP_PORT} ")
if [ -z "$PORT_STATUS" ]; then
    echo "Checking port $APP_PORT... [FAIL] Port not listening!"
    exit 1
else
    echo "Checking port $APP_PORT... [OK]"
fi

echo ""

# =============================================================
# [2] 방화벽 상태 점검 (경고만, 종료 안 함)
# =============================================================
echo "[FIREWALL CHECK]"

# UFW 상태 확인: ufw status → 상태 파일 순으로 폴백 (컨테이너 환경 호환)
UFW_STATUS_FILE="/var/run/ufw-status"
if ufw status 2>/dev/null | grep -q "Status: active"; then
    echo "Firewall (UFW)... [OK] Active"
elif [ -f "$UFW_STATUS_FILE" ] && grep -q "^active" "$UFW_STATUS_FILE"; then
    MODE=$(cat "$UFW_STATUS_FILE")
    echo "Firewall (UFW)... [OK] Active (${MODE})"
else
    echo "[WARNING] Firewall (UFW) is not active!"
fi

echo ""

# =============================================================
# [3] RESOURCE MONITORING - CPU / MEM / DISK 수집
# =============================================================
echo "[RESOURCE MONITORING]"

# CPU 사용률 수집
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")

# 메모리 사용률 수집
MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
MEM_USED=$(free | grep Mem | awk '{print $3}')
if [ "${MEM_TOTAL:-0}" -gt 0 ]; then
    MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEM_USAGE="0.0"
fi

# 디스크 사용률 수집 (루트 파티션)
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""

# =============================================================
# [4] 임계값 경고 (경고만, 종료 안 함)
# =============================================================
CPU_INT=$(echo "$CPU_USAGE" | cut -d'.' -f1)
if [ "${CPU_INT:-0}" -gt "$CPU_THRESHOLD" ]; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
fi

MEM_INT=$(echo "$MEM_USAGE" | cut -d'.' -f1)
if [ "${MEM_INT:-0}" -gt "$MEM_THRESHOLD" ]; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
fi

if [ "${DISK_USAGE:-0}" -gt "$DISK_THRESHOLD" ]; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"
fi

echo ""
echo "===================================="

# =============================================================
# [5] 로그 기록
# =============================================================

# 로그 디렉토리 없으면 생성
LOG_DIR=$(dirname "$LOG_FILE")
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR" 2>/dev/null
fi

# 로그 로테이션 실행 (10MB 초과 시 자동 순환)
rotate_log

# 로그 한 줄 추가 기록 (>> : 누적 기록, > 는 덮어쓰므로 절대 사용 금지)
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
