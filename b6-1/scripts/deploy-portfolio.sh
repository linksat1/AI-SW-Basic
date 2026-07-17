#!/bin/bash
# b4-1 포트폴리오(index.html 등)를 b6-1 EC2 인스턴스(nginx)에 배포하는 스크립트.
# 사전 조건: 가이드.md Step 2~4를 따라 VPC/SG/EC2(Amazon Linux 2023, nginx 설치)가
#           이미 떠 있고, 22번 포트가 본인 IP로 열려 있어야 한다.
#
# 사용법: ./deploy-portfolio.sh <EC2_퍼블릭IP> <PEM_키_경로>
# 예시:   ./deploy-portfolio.sh 13.125.33.210 ~/.ssh/b6-1-key.pem

set -euo pipefail

EC2_IP="${1:?사용법: ./deploy-portfolio.sh <EC2_퍼블릭IP> <PEM_키_경로>}"
PEM_PATH="${2:?사용법: ./deploy-portfolio.sh <EC2_퍼블릭IP> <PEM_키_경로>}"
REMOTE_USER="ec2-user"
PORTFOLIO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../b4-1/portfolio" && pwd)"
SSH_OPTS=(-i "$PEM_PATH" -o StrictHostKeyChecking=accept-new)

echo "==> 로컬 포트폴리오 경로: $PORTFOLIO_DIR"

echo "==> 1. 파일을 EC2의 임시 폴더로 업로드 (rsync)"
rsync -avz --delete \
  --exclude 'index.old.html' \
  --exclude 'convert_png_to_jpg.py' \
  --exclude '.DS_Store' \
  -e "ssh ${SSH_OPTS[*]}" \
  "$PORTFOLIO_DIR/" "$REMOTE_USER@$EC2_IP:/tmp/portfolio/"

echo "==> 2. nginx 문서 루트로 배치 + 재시작"
ssh "${SSH_OPTS[@]}" "$REMOTE_USER@$EC2_IP" '
  sudo rm -rf /usr/share/nginx/html/*
  sudo cp -r /tmp/portfolio/. /usr/share/nginx/html/
  echo "OK" | sudo tee /usr/share/nginx/html/health > /dev/null
  sudo systemctl restart nginx
'

echo "==> 3. 검증"
echo "--- curl -i http://$EC2_IP ---"
curl -is "http://$EC2_IP" | head -n 5
echo
echo "완료. 브라우저에서 http://$EC2_IP 로 접속해 포트폴리오가 뜨는지 확인하세요."
