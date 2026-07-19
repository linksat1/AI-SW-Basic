#!/bin/bash
# 위성 궤도/주파수 SQL 데모(FastAPI)를 b6-1 EC2 인스턴스(visuallsat.com)에 배포하는 스크립트.
# 기존 포트폴리오 사이트(nginx)는 그대로 두고, /sql-demo/ 경로로 백엔드를 추가한다.
#
# 안전장치:
# - 새 인바운드 포트를 열지 않는다 (FastAPI는 127.0.0.1:8000에만 바인딩, 기존 80번 포트로만 노출)
# - 기존 /etc/nginx/nginx.conf는 건드리지 않는다 (default.d/conf.d 드롭인 파일만 추가)
# - 문제가 생기면: `sudo systemctl stop sql-demo && sudo rm /etc/nginx/default.d/sql-demo.conf
#   /etc/nginx/default.d/cloudflare-realip.conf /etc/nginx/conf.d/sql-demo-ratelimit.conf
#   && sudo systemctl reload nginx` 로 완전히 원상복구된다.
#   (cloudflare-realip.conf는 access.log의 IP를 실제 방문자 IP로 복원하는 부작용도 있는데,
#   이건 사이트 전체에 좋은 변경이라 롤백 시에도 굳이 지울 필요는 없다 — 필요하면 지워도 무방)
#
# 사전 조건: rsync가 로컬(Windows)에 없어 scp로 전체 폴더를 복사한다.
#           (b6-1/docs/troubleshooting.md 인지 #6과 동일한 상황)
#
# 사용법: ./deploy-sql-demo.sh <EC2_퍼블릭IP> <PEM_키_경로>
# 예시:   ./deploy-sql-demo.sh <EC2_퍼블릭IP> ~/.ssh/<PEM_키_파일명>.pem
# (실제 IP·키 파일명은 b6-1/AWS자료올리기.md — git 추적 제외 — 참고)

set -euo pipefail

EC2_IP="${1:?사용법: ./deploy-sql-demo.sh <EC2_퍼블릭IP> <PEM_키_경로>}"
PEM_PATH="${2:?사용법: ./deploy-sql-demo.sh <EC2_퍼블릭IP> <PEM_키_경로>}"
REMOTE_USER="ec2-user"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SSH_OPTS=(-i "$PEM_PATH" -o StrictHostKeyChecking=accept-new)

echo "==> 로컬 앱 경로: $APP_DIR"

echo "==> 1. 앱 파일을 EC2 임시 폴더로 업로드 (scp, rsync 미설치 환경 대응)"
ssh "${SSH_OPTS[@]}" "$REMOTE_USER@$EC2_IP" 'rm -rf /tmp/sql-demo-app && mkdir -p /tmp/sql-demo-app'
scp -i "$PEM_PATH" -o StrictHostKeyChecking=accept-new -r \
  "$APP_DIR/app" "$APP_DIR/data" "$APP_DIR/requirements.txt" "$APP_DIR/deploy" \
  "$REMOTE_USER@$EC2_IP:/tmp/sql-demo-app/"

echo "==> 2. 서버에서 설치/설정 (pip, venv, systemd, nginx)"
ssh "${SSH_OPTS[@]}" "$REMOTE_USER@$EC2_IP" '
  set -euo pipefail

  echo "-- python3-pip 확인/설치"
  if ! python3 -m pip --version >/dev/null 2>&1; then
    sudo dnf install -y python3-pip
  fi

  echo "-- 앱 디렉토리 배치 (/opt/sql-demo)"
  sudo mkdir -p /opt/sql-demo /opt/sql-demo/data
  # app/은 코드라 통째로 교체해도 안전하지만, data/는 users.db(회원 DB)와
  # .session_secret(로그인 세션 서명키)이 여기 같이 살고 있어서 통째로 지우면 안 된다.
  # schema.sql/data.sql/.smtp_credentials만 덮어쓰고 나머지 파일(회원 DB 등)은 그대로 둔다.
  # (.smtp_credentials는 서버가 자체 생성하는 게 아니라 로컬이 원본이라 매번 동기화한다)
  sudo rm -rf /opt/sql-demo/app
  sudo cp -r /tmp/sql-demo-app/app /opt/sql-demo/
  sudo cp /tmp/sql-demo-app/data/schema.sql /tmp/sql-demo-app/data/data.sql /opt/sql-demo/data/
  sudo cp /tmp/sql-demo-app/data/.smtp_credentials /opt/sql-demo/data/.smtp_credentials
  sudo cp /tmp/sql-demo-app/requirements.txt /opt/sql-demo/
  sudo chown -R ec2-user:ec2-user /opt/sql-demo
  sudo chmod 600 /opt/sql-demo/data/.smtp_credentials

  echo "-- venv 생성/의존성 설치"
  if [ ! -d /opt/sql-demo/venv ]; then
    python3 -m venv /opt/sql-demo/venv
  fi
  /opt/sql-demo/venv/bin/pip install --quiet --upgrade pip
  /opt/sql-demo/venv/bin/pip install --quiet -r /opt/sql-demo/requirements.txt

  echo "-- systemd 서비스 등록"
  sudo cp /tmp/sql-demo-app/deploy/sql-demo.service /etc/systemd/system/sql-demo.service
  sudo systemctl daemon-reload
  sudo systemctl enable sql-demo
  sudo systemctl restart sql-demo

  echo "-- nginx 설정 (default.d + conf.d 드롭인, 기존 nginx.conf는 변경하지 않음)"
  sudo cp /tmp/sql-demo-app/deploy/sql-demo-nginx.conf /etc/nginx/default.d/sql-demo.conf
  sudo cp /tmp/sql-demo-app/deploy/sql-demo-ratelimit.conf /etc/nginx/conf.d/sql-demo-ratelimit.conf
  sudo cp /tmp/sql-demo-app/deploy/cloudflare-realip.conf /etc/nginx/default.d/cloudflare-realip.conf
  sudo nginx -t
  sudo systemctl reload nginx

  echo "-- 자체 점검"
  sleep 1
  curl -sf http://127.0.0.1:8000/sql-demo/api/queries > /dev/null && echo "FastAPI 자체 응답 OK"
  systemctl is-active sql-demo
'

echo "==> 3. 외부에서 확인"
echo "브라우저에서 http://$EC2_IP/sql-demo/ 또는 http://visuallsat.com/sql-demo/ 로 접속해 확인하세요."
