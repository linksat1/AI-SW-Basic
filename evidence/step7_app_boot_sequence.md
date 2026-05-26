# 7단계: 앱 실행 확인 (Boot Sequence) 증거

## 앱 실행 명령
```bash
sudo -u agent-admin bash -c '
  export AGENT_HOME=/home/agent-admin/agent-app
  export AGENT_PORT=15034
  export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
  export AGENT_KEY_PATH=$AGENT_HOME/api_keys
  export AGENT_LOG_DIR=/var/log/agent-app
  nohup /home/agent-admin/agent-app/agent-app-linux-x86 > /tmp/agent-boot.log 2>&1 &
'
```

## Boot Sequence 출력
```
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/5] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
2026-05-26 20:50:02,562 [INFO] Agent listening at port 15034
```

## 포트 LISTEN 상태
```
tcp  LISTEN  0  1  0.0.0.0:15034  0.0.0.0:*  users:(("agent-app-linux",...))
```

## 참고: AGENT_KEY_PATH 설정
앱 바이너리는 AGENT_KEY_PATH를 **디렉토리 경로**로 처리하며,
해당 디렉토리 내의 `.key` 파일을 자동 탐색합니다.
- `AGENT_KEY_PATH=$AGENT_HOME/api_keys` (디렉토리)
- 내부 파일: `secret.key`, `t_secret.key` (동일 내용: `agent_api_key_test`)

## 검증 결과
- ✅ [1/5] 서비스 계정 agent-admin(uid=1000)으로 실행
- ✅ [2/5] 필수 환경 변수 모두 정상
- ✅ [3/5] 키 파일 내용 검증 완료
- ✅ [4/5] 포트 15034 사용 가능
- ✅ [5/5] 로그 디렉토리 쓰기 가능
- ✅ Agent READY 출력
- ✅ 0.0.0.0:15034 LISTEN 상태
