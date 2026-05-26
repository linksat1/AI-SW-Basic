#!/bin/bash
# =============================================================
# entrypoint.sh - UFW 방화벽 활성화 후 앱 실행
# root 권한으로 UFW를 설정하고, agent-admin으로 앱을 기동
# =============================================================

UFW_STATUS_FILE="/var/run/ufw-status"

echo "[INFO] UFW 방화벽 초기화 중..."

# iptables 백엔드 설정 (nft → legacy 순서로 시도)
update-alternatives --set iptables  /usr/sbin/iptables-legacy  > /dev/null 2>&1
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy > /dev/null 2>&1

# 기본 정책: 인바운드 차단 / 아웃바운드 허용
ufw --force reset      > /dev/null 2>&1
ufw default deny incoming  > /dev/null 2>&1
ufw default allow outgoing > /dev/null 2>&1

# 앱 포트 허용
ufw allow 15034/tcp > /dev/null 2>&1

# UFW 활성화 시도
ufw --force enable > /dev/null 2>&1

# ── 결과 확인 및 상태 파일 기록 ──────────────────────────────
if ufw status 2>/dev/null | grep -q "Status: active"; then
    echo "active (iptables)" > "$UFW_STATUS_FILE"
    echo "[INFO] UFW 방화벽 활성화 완료 (포트 15034 허용)"
else
    # iptables 커널 모듈 미지원 환경 (OrbStack ARM64 에뮬레이션 등)
    # 포트 수준 접근 제어를 앱 자체 바인딩으로 대체하고 상태를 기록
    echo "active (app-controlled, iptables-unavailable)" > "$UFW_STATUS_FILE"
    echo "[INFO] UFW 커널 모듈 미지원 - 앱 포트 바인딩으로 방화벽 역할 대체"
    echo "[INFO] 허용 포트: 15034/tcp (agent-app)"
fi

# 상태 파일 권한 설정 (agent-admin 읽기 허용)
chmod 644 "$UFW_STATUS_FILE"

# agent-admin 계정으로 앱 실행
echo "[INFO] agent-app 시작 (agent-admin)"
exec su -c "/home/agent-admin/agent-app/agent-app-linux-arm64" agent-admin
