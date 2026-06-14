#!/bin/bash

# B1-2 초보자용 모니터링 스크립트
# 목적:
#   agent-leak-app 프로세스가 살아있는지, CPU/MEM을 얼마나 쓰는지,
#   포트 15034를 열고 있는지 주기적으로 로그에 남깁니다.
#
# 사용 예:
#   MONITOR_LOG=evidence_oom_before_monitor.log ./monitor.sh
#
# 멈추는 방법:
#   Ctrl + C

# MONITOR_LOG가 설정되어 있으면 그 파일에 기록합니다.
# 설정되어 있지 않으면 B1-1에서 쓰던 /var/log/agent-app/monitor.log를 기본값으로 사용합니다.
LOG_FILE="${MONITOR_LOG:-${AGENT_LOG_DIR:-/var/log/agent-app}/monitor.log}"

# AGENT_PORT가 설정되어 있으면 그 포트를 확인합니다.
# 설정되어 있지 않으면 미션 기본 포트인 15034를 사용합니다.
PORT="${AGENT_PORT:-15034}"

# 로그 파일이 들어갈 폴더가 없으면 미리 만듭니다.
mkdir -p "$(dirname "$LOG_FILE")"

echo "=== Monitor started at $(date) ===" >> "$LOG_FILE"
echo "LOG_FILE=$LOG_FILE" >> "$LOG_FILE"
echo "PORT=$PORT" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

while true; do
  echo "[$(date)] --- Monitor Snapshot ---" >> "$LOG_FILE"

  # pgrep -x는 이름이 정확히 agent-leak-app인 프로세스의 PID를 찾습니다.
  # || true는 프로세스가 없어도 스크립트가 멈추지 않게 합니다.
  PIDS=$(pgrep -x "agent-leak-app" || true)

  if [ -z "$PIDS" ]; then
    echo "PROCESS: FAIL - agent-leak-app is NOT running" >> "$LOG_FILE"
  else
    echo "PROCESS: OK - agent-leak-app running with PID(s): $PIDS" >> "$LOG_FILE"

    for PID in $PIDS; do
      # ps 컬럼 설명:
      # pid  : 프로세스 ID
      # ppid : 부모 프로세스 ID
      # user : 실행 사용자
      # %cpu : CPU 사용률
      # %mem : 메모리 사용률
      # rss  : 실제 메모리 사용량(KB)
      # stat : 프로세스 상태(S=sleeping, R=running 등)
      # cmd  : 실행 명령
      ps -p "$PID" -o pid,ppid,user,%cpu,%mem,rss,stat,cmd --no-headers >> "$LOG_FILE" 2>/dev/null || true
    done
  fi

  # ss가 있으면 포트가 열려 있는지 확인합니다.
  # 포트가 닫혀 있어도 모든 케이스에서 실패는 아닙니다. 참고 증거로만 봅니다.
  if command -v ss >/dev/null 2>&1; then
    if ss -ltnp 2>/dev/null | grep -q ":$PORT "; then
      echo "PORT: OK - $PORT is listening" >> "$LOG_FILE"
    else
      echo "PORT: WARN - $PORT is not listening" >> "$LOG_FILE"
    fi
  else
    echo "PORT: SKIP - ss command not installed" >> "$LOG_FILE"
  fi

  echo "" >> "$LOG_FILE"

  # 2초마다 반복 측정합니다.
  sleep 2
done
