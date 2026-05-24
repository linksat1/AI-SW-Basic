Last login: Sat May 23 20:12:18 on ttys006
cspag5955@c5r5s1 ~ % >....                                                                                                         
echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/t_secret.key# 키 파일 권한 설정 (소유자만 읽기 가능하도록 보안 강 화)
chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key# 확인
cat /home/agent-admin/agent-app/api_keys/t_secret.key
```**출력:** agent_api_key_test### 6.3 환경 변수 설정환경 변수는 프로그램이 실행될 때 참조하는 설정값입니다.
AGENT_HOME을 설정해두면 경로를 일일이 입력하지 않아도 됩니다.
--
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
EOF# 변경사항 즉시 적용
source /home/agent-admin/.bashrc
--
echo $AGENT_KEY_PATH
```**정상 출력:**

/home/agent-admin/agent-app
--
/home/agent-admin/agent-app/api_keys/t_secret.key
**~/.bashrc란?**
터미널(bash 셸)을 열 때마다 자동으로 실행되는 설정 파일입니다.
여기에 환경 변수를 넣으면 로그인할 때마다 자동으로 설정됩니다.
--
... Verified key file with correct key string.
[4/5] Checking Port Availability          [OK]
... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
--
- [3/5]: 키 파일 경로와 내용 확인 (cat $AGENT_KEY_PATH)
- [4/5]: 15034 포트가 이미 사용 중인지 확인 (ss -tulnp | grep 15034)
- [5/5]: /var/log/agent-app 디렉토리 권한 확인### 7.3 새 터미널에서 앱 실행 상태 확인--
getfacl /home/agent-admin/agent-app/api_keys
getfacl /var/log/agent-app# ✅ 8. 키 파일 확인
cat /home/agent-admin/agent-app/api_keys/t_secret.key
# 출력: agent_api_key_test# ✅ 9. 앱 실행 (별도 터미널에서 실행 중이어야 함)
ps aux | grep agent_app.py
ss -tulnp | grep 15034--
ls -la $AGENT_KEY_PATH
cat $AGENT_KEY_PATH
# 출력이 정확히 "agent_api_key_test" 이어야 합니다 (공백 없이)# 혹시 개행문자가 다를 경우 다시 생성
printf "agent_api_key_test\n" > $AGENT_KEY_PATH
```---## 용어 정리더 보기8:40 PMClaude 응답: 교본에서 찾았어요!교본에서 찾았어요! secret.key 파일을 생성해야 합니다
순서대로 실행하세요:

1. secret.key 파일 생성
bashsudo sh -c 'echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key'
sudo chmod 600 /home/agent-admin/agent-app/api_keys/secret.key
sudo chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/secret.key
2. 로그 디렉토리 생성
bashsudo mkdir -p /var/log/agent-app
sudo chown agent-admin:agent-admin /var/log/agent-app
sudo chmod 770 /var/log/agent-app
3. agent-admin으로 전환 후 환경변수 설정 및 실행
bashsu - agent-admin
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
export AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
cd /home/agent-admin/agent-app
./agent-app-linux-x86

순서대로 실행해보세요! 🚀입력 내용: 이렇게 계속 진행되요이렇게 계속 진행되요8:51 PMClaude 응답: 앱 실행 성공!앱 실행 성공! 🎉 정상 동작 중입니다!
이 로그는 agent-app이 CPU/메모리 부하 테스트를 시뮬레이션하는 것입니다.

로그 의미
로그의미Mode=DOWN부하 감소 중Mode=UP부하 증가 중BOTTOM REACHED최저점 도달 → 다시 증가Memory Increasing/Releasing메모리 시뮬레이션CPU Occupy coreCPU 점유 시뮬레이션

새 터미널 탭에서 앱 상태 확인
Cmd+T 새 탭 열고:
bashssh b1-lab@orb
zsh: event not found: 입력
cspag5955@c5r5s1 ~ % ps aux | grep agent-app
cspag5955        36739   0.0  0.0 34691288    608 s007  U+    8:57PM   0:00.00 grep agent-app
cspag5955@c5r5s1 ~ % ss -tulnp | grep 15034
zsh: command not found: ss
cspag5955@c5r5s1 ~ % 
  [Restored May 24, 2026 at 2:49:14 PM]
Last login: Sun May 24 14:49:10 on console
cspag5955@c5r5s1 ~ % 








