# 6단계: 앱 실행 환경 구성 증거

## 환경 변수 설정 위치
- `/home/agent-admin/.bashrc` (인터랙티브 셸용)
- `/etc/profile.d/agent-env.sh` (모든 로그인 셸 공통 적용)

## 환경 변수 목록
```
AGENT_HOME=/home/agent-admin/agent-app
AGENT_PORT=15034
AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys/t_secret.key
AGENT_LOG_DIR=/var/log/agent-app
```

## 키 파일
```
경로: /home/agent-admin/agent-app/api_keys/t_secret.key
내용: agent_api_key_test
권한: -rw------- (600) - 소유자만 읽기 가능
```

## api_keys 디렉토리 내용
```
-rw-------  agent-admin  agent-admin  secret.key
-rw-------  agent-admin  agent-admin  t_secret.key
```

## 검증 결과
- ✅ AGENT_HOME=/home/agent-admin/agent-app
- ✅ AGENT_PORT=15034
- ✅ AGENT_KEY_PATH 파일 경로 포함
- ✅ t_secret.key 내용: agent_api_key_test
- ✅ /etc/profile.d/agent-env.sh 시스템 공통 적용
