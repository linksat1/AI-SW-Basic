FROM ubuntu:24.04

# 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    acl \
    net-tools \
    iproute2 \
    ufw \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# 그룹 생성 (계정보다 먼저)
RUN groupadd agent-common && \
    groupadd agent-core

# Ubuntu 24.04의 기본 ubuntu 사용자(uid=1000)를 agent-admin으로 rename
RUN usermod -l agent-admin -d /home/agent-admin -m ubuntu && \
    groupmod -n agent-admin ubuntu && \
    usermod -s /bin/bash agent-admin && \
    usermod -aG agent-common,agent-core agent-admin

# 스크립트 소유자용 agent-dev 계정 생성
RUN useradd -m -s /bin/bash -G agent-common,agent-core agent-dev

# 디렉토리 구조 생성
RUN mkdir -p /home/agent-admin/agent-app/upload_files \
             /home/agent-admin/agent-app/api_keys \
             /home/agent-admin/agent-app/bin \
             /var/log/agent-app \
             /var/log/monitor/agent-app/archive

# 소유자/그룹 설정
RUN chown -R agent-admin:agent-admin /home/agent-admin/agent-app && \
    chown agent-admin:agent-common    /home/agent-admin/agent-app/upload_files && \
    chown agent-admin:agent-core      /home/agent-admin/agent-app/api_keys && \
    chown agent-admin:agent-core      /var/log/agent-app && \
    chown -R agent-admin:agent-core   /var/log/monitor

# 권한 설정
RUN chmod 2775 /home/agent-admin/agent-app/upload_files && \
    chmod 750   /home/agent-admin/agent-app/api_keys && \
    chmod 770   /var/log/agent-app && \
    chmod -R 770 /var/log/monitor

# ACL 설정
RUN setfacl -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files && \
    setfacl -d -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files && \
    setfacl -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys && \
    setfacl -d -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys && \
    setfacl -m g:agent-core:rwx /var/log/agent-app && \
    setfacl -d -m g:agent-core:rwx /var/log/agent-app

# 앱 바이너리 복사 (빌드 컨텍스트: 프로젝트 루트)
COPY agent-app/agent-app-linux-arm64 /home/agent-admin/agent-app/agent-app-linux-arm64
RUN chmod +x /home/agent-admin/agent-app/agent-app-linux-arm64 && \
    chown agent-admin:agent-admin /home/agent-admin/agent-app/agent-app-linux-arm64

# 운영 스크립트 복사 (소유자: agent-dev, 그룹: agent-core, 권한: 750)
COPY scripts/monitor.sh     /home/agent-admin/agent-app/bin/monitor.sh
COPY scripts/report.sh      /home/agent-admin/agent-app/bin/report.sh
COPY scripts/log_archive.sh /home/agent-admin/agent-app/bin/log_archive.sh
RUN chown agent-dev:agent-core /home/agent-admin/agent-app/bin/*.sh && \
    chmod 750                  /home/agent-admin/agent-app/bin/*.sh

# entrypoint 스크립트 복사 (root 소유, UFW 활성화 후 앱 기동)
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

# 키 파일 생성
RUN echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key && \
    chmod 600 /home/agent-admin/agent-app/api_keys/secret.key && \
    chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/secret.key

# 환경 변수 설정
ENV AGENT_HOME=/home/agent-admin/agent-app
ENV AGENT_PORT=15034
ENV AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
ENV AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
ENV AGENT_LOG_DIR=/var/log/agent-app

# 포트 노출
EXPOSE 15034

# entrypoint: root로 UFW 활성화 → agent-admin으로 앱 기동
WORKDIR /home/agent-admin/agent-app

CMD ["/entrypoint.sh"]
