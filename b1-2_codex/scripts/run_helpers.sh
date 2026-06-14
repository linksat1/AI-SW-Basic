#!/bin/bash

# B1-2 실습 보조 함수 모음
# 사용법:
#   source ./run_helpers.sh
#   set_common_env
#   start_monitor evidence/logs/oom_before_monitor.log
#   ./agent-leak-app 2>&1 | tee /var/log/agent-app/oom_before_app.log
#   stop_monitor

start_monitor() {
  local log_file="$1"

  # 로그 저장 폴더가 없으면 만듭니다.
  mkdir -p "$(dirname "$log_file")"

  # 기존 로그 내용을 비우고 새로 시작합니다.
  : > "$log_file"

  # monitor.sh를 백그라운드에서 실행합니다.
  # &를 붙이면 현재 터미널을 계속 사용할 수 있습니다.
  MONITOR_LOG="$log_file" AGENT_PORT="${AGENT_PORT:-15034}" ./monitor.sh &

  # 방금 실행한 백그라운드 프로세스의 PID를 저장합니다.
  MONITOR_PID=$!
  echo "$MONITOR_PID" > /tmp/b12_monitor.pid
  echo "Started monitor PID=$MONITOR_PID, log=$log_file"
}

stop_monitor() {
  # 저장해 둔 monitor PID가 있으면 그 프로세스를 종료합니다.
  if [ -f /tmp/b12_monitor.pid ]; then
    kill "$(cat /tmp/b12_monitor.pid)" 2>/dev/null || true
    rm -f /tmp/b12_monitor.pid
  fi

  # 혹시 남아있는 monitor.sh도 정리합니다.
  pkill -f monitor.sh 2>/dev/null || true
  echo "Stopped monitor"
}

cleanup_app() {
  # agent-leak-app이 여러 개 떠 있으면 실습 결과가 헷갈립니다.
  # 새 케이스를 시작하기 전에 정리합니다.
  pkill -f agent-leak-app 2>/dev/null || true
  sleep 2
}

set_common_env() {
  # B1-1에서 만든 환경을 기준으로 앱 부팅에 필요한 공통 환경변수를 설정합니다.
  export AGENT_HOME=/home/agent-admin/agent-app
  export AGENT_LOG_DIR=/var/log/agent-app
  export AGENT_PORT=15034
  export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files

  # B1-2 앱은 secret.key가 들어 있는 api_keys 디렉터리를 요구합니다.
  # B1-1의 t_secret.key 파일 경로와 헷갈리지 않도록 디렉터리로 지정합니다.
  export AGENT_KEY_PATH=$AGENT_HOME/api_keys
}

get_app_pid() {
  # 이름이 정확히 agent-leak-app인 PID 중 마지막 값을 가져옵니다.
  # 부모/자식 프로세스가 함께 보일 수 있으므로 실제 실습에서는 ps로 한 번 더 확인하세요.
  pgrep -x agent-leak-app | tail -n 1
}

show_app_ps() {
  # 현재 agent-leak-app 프로세스의 자원 사용량을 한 번에 확인합니다.
  ps -C agent-leak-app -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
}
