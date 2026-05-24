Last login: Sat May 23 20:09:13 on ttys002
cspag5955@c5r5s1 ~ % orb push b1-lab ~/Downloads/agent-app.zip /tmp/agent-app.zip

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cp: target '/tmp/agent-app.zip': No such file or directory
cspag5955@c5r5s1 ~ % scp ~/Downloads/agent-app.zip cspag5955@b1-lab.orb.local:/tmp/
ssh: connect to host b1-lab.orb.local port 22: Operation timed out
scp: Connection closed
cspag5955@c5r5s1 ~ % scp -P 20022 ~/Downloads/agent-app.zip cspag5955@b1-lab.orb.local:/tmp/
The authenticity of host '[b1-lab.orb.local]:20022 ([192.168.138.3]:20022)' can't be established.
ED25519 key fingerprint is SHA256:UaUiQ1EaxNRGU6lL9KBWEpUyzy1CanWms2lG+otjq/I.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[b1-lab.orb.local]:20022' (ED25519) to the list of known hosts.
cspag5955@b1-lab.orb.local's password: 
Permission denied, please try again.
cspag5955@b1-lab.orb.local's password: 
Permission denied, please try again.
cspag5955@b1-lab.orb.local's password: 
cspag5955@b1-lab.orb.local: Permission denied (publickey,password,keyboard-interactive).
scp: Connection closed
cspag5955@c5r5s1 ~ % orb push b1-lab ~/Downloads/agent-app.zip /home/cspag5955/agent-app.zip

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cp: target '/home/cspag5955/agent-app.zip': No such file or directory
cspag5955@c5r5s1 ~ % ls ~/.orbstack/ssh/
authorized_keys	config		id_ed25519	id_ed25519.pub	known_hosts
cspag5955@c5r5s1 ~ % scp -P 20022 -i ~/.orbstack/ssh/id_ed25519 ~/Downloads/agent-app.zip cspag5955@b1-lab.orb.local:/tmp/
cspag5955@b1-lab.orb.local's password: 
Permission denied, please try again.
cspag5955@b1-lab.orb.local's password: 
Permission denied, please try again.
cspag5955@b1-lab.orb.local's password: 
cspag5955@b1-lab.orb.local: Permission denied (publickey,password,keyboard-interactive).
scp: Connection closed
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ cd /tmp
ls
cc-daemon-1267600670  claude-1267600670
cspag5955@b1-lab:/tmp$ orb push b1-lab ~/Downloads/agent-app.zip /tmp/agent-app.zip

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cp: target '/tmp/agent-app.zip': No such file or directory
cspag5955@b1-lab:/tmp$ ls /tmp/agent-app.zip
ls: cannot access '/tmp/agent-app.zip': No such file or directory
cspag5955@b1-lab:/tmp$ ls
cc-daemon-1267600670  claude-1267600670
cspag5955@b1-lab:/tmp$ sudo find / -name "agent-app.zip" 2>/dev/null
/mnt/mac/System/Volumes/Data/Users/cspag5955/Downloads/agent-app.zip
/mnt/mac/Users/cspag5955/Downloads/agent-app.zip
/Users/cspag5955/Downloads/agent-app.zip
cspag5955@b1-lab:/tmp$ cp /mnt/mac/Users/cspag5955/Downloads/agent-app.zip /tmp/
cspag5955@b1-lab:/tmp$ ls /tmp/agent-app.zip
/tmp/agent-app.zip
cspag5955@b1-lab:/tmp$ sudo adduser agent-admin
adduser: The user `agent-admin' already exists.
cspag5955@b1-lab:/tmp$ sudo mkdir -p /home/agent-admin/agent-app
cspag5955@b1-lab:/tmp$ sudo unzip /tmp/agent-app.zip -d /home/agent-admin/agent-app/
Archive:  /tmp/agent-app.zip
  inflating: /home/agent-admin/agent-app/agent-app-linux-x86  
  inflating: /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-x86  
  inflating: /home/agent-admin/agent-app/agent-app-linux-arm64  
  inflating: /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-arm64  
cspag5955@b1-lab:/tmp$ ls /home/agent-admin/agent-app/
ls: cannot access '/home/agent-admin/agent-app/': Permission denied
cspag5955@b1-lab:/tmp$ sudo ls /home/agent-admin/agent-app/
__MACOSX  agent-app-linux-arm64  agent-app-linux-x86  api_keys	bin  upload_files
cspag5955@b1-lab:/tmp$ sudo chown -R agent-admin:agent-admin /home/agent-admin/agent-app/
cspag5955@b1-lab:/tmp$ sudo chmod +x /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/tmp$ sudo ls /home/agent-admin/agent-app/
__MACOSX  agent-app-linux-arm64  agent-app-linux-x86  api_keys	bin  upload_files
cspag5955@b1-lab:/tmp$ 
cspag5955@b1-lab:/tmp$ 
cspag5955@b1-lab:/tmp$ 
cspag5955@b1-lab:/tmp$ su - agent-admin
Password: 
su: Authentication failure
cspag5955@b1-lab:/tmp$ sudo passwd agent-admin
New password: 
Retype new password: 
passwd: password updated successfully
cspag5955@b1-lab:/tmp$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
./agent-app-linux-arm64
[qemu-arm64]: Could not open '/lib/ld-linux-aarch64.so.1': No such file or directory
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [FAIL]
   >>> Critical Env 'AGENT_HOME' is missing.
Traceback (most recent call last):
  File "linux_pbl.py", line 456, in <module>
  File "linux_pbl.py", line 156, in check_required_files
  File "posixpath.py", line 76, in join
TypeError: expected str, bytes or os.PathLike object, not NoneType
[PYI-15407:ERROR] Failed to execute script 'linux_pbl' due to unhandled exception!
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ export AGENT_HOME=/home/agent-admin/agent-app
./agent-app-linux-x86
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [FAIL]
   >>> Missing Env: AGENT_PORT
   >>> Missing Env: AGENT_UPLOAD_DIR
   >>> Missing Env: AGENT_KEY_PATH
[3/5] Checking Required Files             [FAIL]
   >>> Skipped due to previous critical failure.
[4/5] Checking Port Availability          [FAIL]
   >>> Skipped due to previous critical failure.
[5/5] Verifying Log Permission            [FAIL]
   >>> Skipped due to previous critical failure.
--------------------------------------------------
System Boot Failed. Process Terminated.
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
export AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys/t_secret.key
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [FAIL]
   >>> Key Path Mismatch. Expected: /home/agent-admin/agent-app/api_keys
[3/5] Checking Required Files             [FAIL]
   >>> Skipped due to previous critical failure.
[4/5] Checking Port Availability          [FAIL]
   >>> Skipped due to previous critical failure.
[5/5] Verifying Log Permission            [FAIL]
   >>> Skipped due to previous critical failure.
--------------------------------------------------
System Boot Failed. Process Terminated.
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ export AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
./agent-app-linux-x86
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [FAIL]
   >>> Missing File: secret.key
   >>>    (Expected location: /home/agent-admin/agent-app/api_keys/secret.key)
[4/5] Checking Port Availability          [FAIL]
   >>> Skipped due to previous critical failure.
[5/5] Verifying Log Permission            [FAIL]
   >>> Skipped due to previous critical failure.
--------------------------------------------------
System Boot Failed. Process Terminated.
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ # api_keys 폴더 내용 확인
ls /home/agent-admin/agent-app/api_keys/
agent-admin@b1-lab:~/agent-app$ ls /home/agent-admin/agent-app/api_keys/
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ cat ~/../../home/cspag5955/AI-SW-Basic/B1-1-selfstudy.md | grep -A5 "secret"
cat: /home/agent-admin/../../home/cspag5955/AI-SW-Basic/B1-1-selfstudy.md: Permission denied
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ sudo cat /home/cspag5955/AI-SW-Basic/B1-1-selfstudy.md | grep -A5 -i "secret\|key"
[sudo] password for agent-admin: 

Sorry, try again.
[sudo] password for agent-admin: 
Sorry, try again.
[sudo] password for agent-admin: 
sudo: 3 incorrect password attempts
agent-admin@b1-lab:~/agent-app$ ssh b1-lab@orb
ssh: Could not resolve hostname orb: Name or service not known
agent-admin@b1-lab:~/agent-app$ exit
logout
agent-admin@b1-lab:~$ exit
logout
cspag5955@b1-lab:/tmp$ exit
logout
Connection to 127.0.0.1 closed.
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ grep -A5 -i "secret\|key" /home/cspag5955/AI-SW-Basic/B1-1-selfstudy.md
sudo mkdir -p /home/agent-admin/agent-app/api_keys
sudo mkdir -p /home/agent-admin/agent-app/bin

# 로그 디렉토리 생성
sudo mkdir -p /var/log/agent-app
```
--
# api_keys: 그룹을 agent-core로 설정
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: 그룹을 agent-core로 설정
sudo chown agent-admin:agent-core /var/log/agent-app
```

--
# api_keys: 소유자만 완전 권한, 그룹은 읽기만, 외부 차단
sudo chmod 750 /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: 그룹(agent-core)이 읽기/쓰기 가능
sudo chmod 770 /var/log/agent-app
```

--
# api_keys: agent-core 그룹에만 읽기/쓰기 허용
sudo setfacl -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys
sudo setfacl -d -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: agent-core 그룹에 읽기/쓰기 허용
sudo setfacl -m g:agent-core:rwx /var/log/agent-app
sudo setfacl -d -m g:agent-core:rwx /var/log/agent-app
```
--
getfacl /home/agent-admin/agent-app/api_keys
getfacl /var/log/agent-app
```

---

--
# api_keys 디렉토리에 키 파일 생성
echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/t_secret.key

# 키 파일 권한 설정 (소유자만 읽기 가능하도록 보안 강화)
chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key

# 확인
cat /home/agent-admin/agent-app/api_keys/t_secret.key
```

**출력:** `agent_api_key_test`

### 6.3 환경 변수 설정

환경 변수는 프로그램이 실행될 때 참조하는 설정값입니다.
`AGENT_HOME`을 설정해두면 경로를 일일이 입력하지 않아도 됩니다.
--
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
EOF

# 변경사항 즉시 적용
source /home/agent-admin/.bashrc
--
echo $AGENT_KEY_PATH
```

**정상 출력:**
```
/home/agent-admin/agent-app
--
/home/agent-admin/agent-app/api_keys/t_secret.key
```

> **`~/.bashrc`란?**
> 터미널(bash 셸)을 열 때마다 자동으로 실행되는 설정 파일입니다.
> 여기에 환경 변수를 넣으면 로그인할 때마다 자동으로 설정됩니다.
--
... Verified key file with correct key string.
[4/5] Checking Port Availability          [OK]
... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
--
> - `[3/5]`: 키 파일 경로와 내용 확인 (`cat $AGENT_KEY_PATH`)
> - `[4/5]`: 15034 포트가 이미 사용 중인지 확인 (`ss -tulnp | grep 15034`)
> - `[5/5]`: `/var/log/agent-app` 디렉토리 권한 확인

### 7.3 새 터미널에서 앱 실행 상태 확인

--
getfacl /home/agent-admin/agent-app/api_keys
getfacl /var/log/agent-app

# ✅ 8. 키 파일 확인
cat /home/agent-admin/agent-app/api_keys/t_secret.key
# 출력: agent_api_key_test

# ✅ 9. 앱 실행 (별도 터미널에서 실행 중이어야 함)
ps aux | grep agent_app.py
ss -tulnp | grep 15034

--
ls -la $AGENT_KEY_PATH
cat $AGENT_KEY_PATH
# 출력이 정확히 "agent_api_key_test" 이어야 합니다 (공백 없이)

# 혹시 개행문자가 다를 경우 다시 생성
printf "agent_api_key_test\n" > $AGENT_KEY_PATH
```

---

## 용어 정리
cspag5955@b1-lab:~$ sudo sh -c 'echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key'
sudo chmod 600 /home/agent-admin/agent-app/api_keys/secret.key
sudo chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/secret.key
cspag5955@b1-lab:~$ sudo sh -c 'echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key'
cspag5955@b1-lab:~$ sudo chmod 600 /home/agent-admin/agent-app/api_keys/secret.key
cspag5955@b1-lab:~$ sudo chown agent-admin:agent-admin /home/agent-admin/agent-app/api_keys/secret.key
cspag5955@b1-lab:~$ sudo mkdir -p /var/log/agent-app
cspag5955@b1-lab:~$ sudo chown agent-admin:agent-admin /var/log/agent-app
cspag5955@b1-lab:~$ sudo chmod 770 /var/log/agent-app
cspag5955@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ export AGENT_HOME=/home/agent-admin/agent-app
agent-admin@b1-lab:~$ export AGENT_PORT=15034
agent-admin@b1-lab:~$ export AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
agent-admin@b1-lab:~$ export AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ cd /home/agent-admin/agent-app
./agent-app-linux-x86
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
2026-05-23 20:44:06,060 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-05-23 20:44:06,061 [INFO] Agent listening at port 15034
2026-05-23 20:44:06,061 [INFO] === Agent Worker Started ===
2026-05-23 20:44:06,061 [INFO]    > Cycle: 0 -> 256MB/Lv10 -> 0
2026-05-23 20:44:06,061 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:44:06,098 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:44:06,098 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:44:08,106 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:44:08,146 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:44:08,146 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:44:11,153 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:44:11,207 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:44:11,207 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:44:15,214 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:44:15,252 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:44:15,252 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:44:20,260 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:44:20,297 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:44:20,297 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:44:26,304 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:44:26,343 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:44:26,343 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:44:32,350 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:44:32,393 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:44:32,393 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:44:38,399 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:44:38,438 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:44:38,438 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:44:44,445 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:44:44,485 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:44:44,485 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:44:50,494 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:44:50,534 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:44:50,534 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:44:56,541 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:44:56,582 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:44:56,582 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:45:02,590 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:45:02,590 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:45:02,592 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:45:02,592 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:45:08,598 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:45:08,601 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:45:08,601 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:45:14,603 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:45:14,604 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:45:14,605 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:45:20,612 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:45:20,613 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:45:20,614 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:45:26,619 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:45:26,620 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:45:26,620 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:45:32,627 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:45:32,629 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:45:32,629 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:45:37,632 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:45:37,633 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:45:37,634 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:45:41,641 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:45:41,642 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:45:41,642 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:45:44,649 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:45:44,650 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:45:44,650 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:45:46,656 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:45:46,658 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:45:47,664 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:45:47,665 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:45:48,672 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:45:48,672 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:45:48,677 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:45:48,677 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:45:50,682 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:45:50,687 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:45:50,687 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:45:53,693 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:45:53,731 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:45:53,732 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:45:57,738 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:45:57,776 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:45:57,777 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:46:02,783 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:46:02,820 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:46:02,821 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:46:08,829 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:46:08,867 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:46:08,868 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:46:14,874 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:46:14,912 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:46:14,912 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:46:20,919 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:46:20,957 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:46:20,957 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:46:26,963 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:46:27,002 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:46:27,002 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:46:33,009 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:46:33,047 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:46:33,048 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:46:39,055 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:46:39,092 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:46:39,093 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:46:45,099 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:46:45,100 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:46:45,100 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:46:45,100 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:46:51,107 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:46:51,109 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:46:51,109 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:46:57,113 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:46:57,113 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:46:57,113 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:47:03,121 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:47:03,123 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:47:03,124 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:47:09,130 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:47:09,131 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:47:09,131 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:47:15,138 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:47:15,140 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:47:15,140 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:47:20,147 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:47:20,148 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:47:20,148 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:47:24,154 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:47:24,156 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:47:24,156 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:47:27,164 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:47:27,164 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:47:27,164 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:47:29,171 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:47:29,173 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:47:30,179 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:47:30,179 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:47:31,185 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:47:31,187 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:47:31,191 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:47:31,191 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:47:33,197 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:47:33,202 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:47:33,202 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:47:36,210 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:47:36,216 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:47:36,216 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:47:40,224 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:47:40,262 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:47:40,262 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:47:45,268 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:47:45,307 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:47:45,307 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:47:51,315 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:47:51,353 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:47:51,353 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:47:57,359 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:47:57,397 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:47:57,397 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:48:03,404 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:48:03,442 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:48:03,442 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:48:09,446 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:48:09,484 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:48:09,485 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:48:15,492 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:48:15,530 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:48:15,530 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:48:21,536 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:48:21,574 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:48:21,574 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:48:27,581 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:48:27,582 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:48:27,582 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:48:27,582 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:48:33,589 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:48:33,591 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:48:33,591 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:48:39,600 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:48:39,600 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:48:39,600 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:48:45,607 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:48:45,609 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:48:45,609 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:48:51,616 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:48:51,616 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:48:51,617 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:48:57,624 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:48:57,626 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:48:57,626 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:49:02,634 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:49:02,634 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:49:02,634 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:49:06,642 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:49:06,644 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:49:06,644 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:49:09,652 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:49:09,652 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:49:09,653 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:49:11,660 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:49:11,662 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:49:12,668 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:49:12,669 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:49:13,675 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:49:13,676 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:49:13,678 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:49:13,678 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:49:15,685 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:49:15,724 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:49:15,724 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:49:18,731 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:49:18,769 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:49:18,769 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:49:22,777 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:49:22,814 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:49:22,815 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:49:27,822 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:49:27,860 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:49:27,860 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:49:33,866 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:49:33,905 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:49:33,905 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:49:39,912 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:49:39,951 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:49:39,951 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:49:45,955 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:49:45,993 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:49:45,993 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:49:52,000 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:49:52,038 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:49:52,038 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:49:58,045 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:49:58,082 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:49:58,082 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:50:04,090 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:50:04,128 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:50:04,128 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:50:10,131 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:50:10,132 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:50:10,132 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:50:10,132 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:50:16,139 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:50:16,141 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:50:16,141 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:50:22,148 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:50:22,148 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:50:22,148 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:50:28,153 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:50:28,155 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:50:28,155 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:50:34,163 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:50:34,163 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:50:34,163 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:50:40,170 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:50:40,172 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:50:40,172 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:50:45,180 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:50:45,180 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:50:45,180 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:50:49,187 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:50:49,189 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:50:49,189 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:50:52,197 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:50:52,198 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:50:52,198 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:50:54,207 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:50:54,209 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:50:55,216 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:50:55,217 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:50:56,223 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:50:56,224 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:50:56,226 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:50:56,226 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:50:58,233 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:50:58,274 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:50:58,274 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:51:01,282 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:51:01,320 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:51:01,320 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:51:05,327 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:51:05,365 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:51:05,366 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:51:10,374 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:51:10,412 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:51:10,412 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:51:16,421 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:51:16,459 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:51:16,459 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:51:22,466 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:51:22,506 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:51:22,506 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:51:28,513 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:51:28,550 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:51:28,550 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:51:34,557 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:51:34,598 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:51:34,599 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:51:40,605 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:51:40,642 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:51:40,643 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:51:46,650 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:51:46,689 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:51:46,689 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:51:52,697 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:51:52,698 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:51:52,698 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:51:52,698 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:51:58,706 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:51:58,708 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:51:58,709 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:52:04,716 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:52:04,716 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:52:04,716 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:52:10,722 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:52:10,723 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:52:10,723 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:52:16,731 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:52:16,731 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:52:16,731 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:52:22,739 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:52:22,743 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:52:22,743 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:52:27,750 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:52:27,750 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:52:27,751 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:52:31,757 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:52:31,759 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:52:31,759 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:52:34,766 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:52:34,766 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:52:34,766 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:52:36,773 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:52:36,775 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:52:37,780 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:52:37,781 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:52:38,788 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:52:38,788 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:52:38,790 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:52:38,791 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:52:40,797 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:52:40,836 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:52:40,836 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:52:43,838 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:52:43,877 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:52:43,877 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:52:47,885 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:52:47,923 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:52:47,923 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:52:52,931 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:52:52,970 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:52:52,970 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:52:58,972 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:52:59,010 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:52:59,010 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:53:05,017 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:53:05,055 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:53:05,055 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:53:11,061 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:53:11,100 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:53:11,100 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:53:17,106 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:53:17,144 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:53:17,144 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:53:23,151 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:53:23,188 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:53:23,189 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:53:29,195 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:53:29,232 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:53:29,232 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:53:35,239 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:53:35,240 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:53:35,240 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:53:35,240 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:53:41,247 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:53:41,249 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:53:41,249 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:53:47,257 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:53:47,257 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:53:47,257 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:53:53,264 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:53:53,266 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:53:53,266 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:53:59,274 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:53:59,274 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:53:59,274 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:54:05,281 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:54:05,283 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:54:05,283 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:54:10,291 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:54:10,291 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:54:10,292 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:54:14,300 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:54:14,302 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:54:14,303 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:54:17,310 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:54:17,310 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:54:17,310 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:54:19,316 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:54:19,318 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:54:20,324 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:54:20,324 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:54:21,327 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:54:21,327 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:54:21,329 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:54:21,329 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:54:23,336 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:54:23,375 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:54:23,375 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:54:26,382 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:54:26,421 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:54:26,421 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:54:30,428 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:54:30,466 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:54:30,466 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:54:35,472 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:54:35,513 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:54:35,513 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:54:41,516 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:54:41,554 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:54:41,554 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:54:47,561 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:54:47,599 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:54:47,599 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:54:53,601 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:54:53,639 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:54:53,639 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:54:59,641 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:54:59,679 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:54:59,679 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:55:05,686 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:55:05,724 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:55:05,724 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:55:11,731 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:55:11,770 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:55:11,770 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:55:17,774 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:55:17,774 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:55:17,774 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:55:17,774 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:55:23,780 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:55:23,782 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:55:23,782 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:55:29,790 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:55:29,790 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:55:29,790 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:55:35,797 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:55:35,799 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:55:35,799 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:55:41,806 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:55:41,806 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:55:41,807 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:55:47,815 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:55:47,817 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:55:47,817 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:55:52,824 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:55:52,824 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:55:52,824 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:55:56,832 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:55:56,834 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:55:56,834 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:55:59,840 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:55:59,841 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:55:59,841 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:56:01,848 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:56:01,850 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:56:02,855 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:56:02,855 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:56:03,861 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:56:03,862 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:56:03,864 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:56:03,864 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:56:05,871 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:56:05,908 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:56:05,909 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:56:08,915 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:56:08,953 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:56:08,953 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:56:12,960 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:56:12,998 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:56:12,998 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:56:18,005 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:56:18,028 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:56:18,028 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:56:24,036 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:56:24,074 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:56:24,074 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:56:30,075 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:56:30,113 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:56:30,113 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:56:36,117 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:56:36,154 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:56:36,155 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:56:42,166 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:56:42,204 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:56:42,204 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:56:48,211 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:56:48,249 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:56:48,249 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:56:54,252 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:56:54,290 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:56:54,290 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:57:00,297 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:57:00,298 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:57:00,298 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:57:00,298 [INFO] [CPU] Occupy core for 5s (Level 9)
^T2026-05-23 20:57:06,304 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:57:06,306 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:57:06,306 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:57:12,312 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:57:12,312 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:57:12,312 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:57:18,313 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:57:18,315 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:57:18,315 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:57:24,322 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:57:24,322 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:57:24,323 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:57:30,331 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:57:30,333 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:57:30,333 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:57:35,340 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:57:35,340 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:57:35,340 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:57:39,347 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:57:39,349 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:57:39,349 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:57:42,350 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:57:42,351 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:57:42,351 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:57:44,357 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:57:44,359 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:57:45,366 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:57:45,366 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:57:46,371 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:57:46,371 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:57:46,373 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:57:46,373 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:57:48,380 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:57:48,419 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:57:48,419 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:57:51,426 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:57:51,463 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:57:51,463 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:57:55,471 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:57:55,510 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:57:55,510 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:58:00,517 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:58:00,555 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:58:00,556 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:58:06,563 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:58:06,604 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:58:06,604 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:58:12,611 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:58:12,649 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:58:12,649 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:58:18,656 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 20:58:18,695 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 20:58:18,695 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:58:24,706 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 20:58:24,745 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 20:58:24,746 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:58:30,753 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 20:58:30,792 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 20:58:30,792 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:58:36,799 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 20:58:36,840 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 20:58:36,841 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 20:58:42,844 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 20:58:42,845 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 20:58:42,845 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 20:58:42,845 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 20:58:48,848 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 20:58:48,849 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 20:58:48,850 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 20:58:54,856 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 20:58:54,856 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 20:58:54,856 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 20:59:00,858 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 20:59:00,859 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 20:59:00,859 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:59:06,866 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 20:59:06,866 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 20:59:06,866 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:59:12,874 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 20:59:12,875 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 20:59:12,876 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:59:17,881 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 20:59:17,881 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 20:59:17,881 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:59:21,888 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 20:59:21,891 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 20:59:21,891 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:59:24,898 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 20:59:24,898 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 20:59:24,899 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:59:26,906 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 20:59:26,908 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 20:59:27,911 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 20:59:27,911 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 20:59:28,917 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 20:59:28,917 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 20:59:28,919 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 20:59:28,919 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 20:59:30,926 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 20:59:30,931 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 20:59:30,932 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 20:59:33,939 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 20:59:33,957 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 20:59:33,957 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 20:59:37,964 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 20:59:37,987 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 20:59:37,987 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 20:59:42,993 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 20:59:43,030 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 20:59:43,030 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 20:59:49,035 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 20:59:49,079 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 20:59:49,079 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 20:59:55,086 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 20:59:55,119 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 20:59:55,119 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:00:01,122 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:00:01,157 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:00:01,157 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:00:07,164 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:00:07,195 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:00:07,195 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:00:13,202 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:00:13,239 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:00:13,239 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:00:19,247 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:00:19,286 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:00:19,286 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:00:25,294 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:00:25,295 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:00:25,295 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:00:25,295 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:00:31,303 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:00:31,305 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:00:31,305 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:00:37,311 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:00:37,311 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:00:37,311 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:00:43,319 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:00:43,322 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:00:43,322 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:00:49,328 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:00:49,328 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:00:49,329 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:00:55,333 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:00:55,335 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:00:55,335 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:01:00,342 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:01:00,342 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:01:00,343 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:01:04,349 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:01:04,351 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:01:04,351 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:01:07,358 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:01:07,358 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:01:07,358 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:01:09,365 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:01:09,368 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:01:10,374 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:01:10,374 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:01:11,380 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:01:11,380 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:01:11,383 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:01:11,383 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:01:13,391 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:01:13,429 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:01:13,429 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:01:16,437 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:01:16,475 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:01:16,475 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:01:20,482 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:01:20,522 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:01:20,522 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:01:25,529 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:01:25,562 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:01:25,562 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:01:31,582 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:01:31,627 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:01:31,627 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:01:37,634 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:01:37,673 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:01:37,673 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:01:43,679 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:01:43,717 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:01:43,717 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:01:49,721 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:01:49,759 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:01:49,759 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:01:55,766 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:01:55,805 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:01:55,805 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:02:01,813 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:02:01,851 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:02:01,852 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:02:07,859 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:02:07,859 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:02:07,859 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:02:07,859 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:02:13,867 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:02:13,869 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:02:13,869 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:02:19,875 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:02:19,875 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:02:19,876 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:02:25,883 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:02:25,885 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:02:25,885 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:02:31,893 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:02:31,893 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:02:31,893 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:02:37,899 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:02:37,901 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:02:37,902 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:02:42,909 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:02:42,910 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:02:42,910 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:02:46,918 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:02:46,920 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:02:46,920 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:02:49,927 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:02:49,927 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:02:49,927 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:02:51,933 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:02:51,934 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:02:52,941 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:02:52,941 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:02:53,947 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:02:53,947 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:02:53,949 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:02:53,949 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:02:55,955 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:02:55,993 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:02:55,994 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:02:58,998 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:02:59,035 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:02:59,035 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:03:03,042 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:03:03,080 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:03:03,080 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:03:08,087 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:03:08,124 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:03:08,124 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:03:14,130 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:03:14,169 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:03:14,170 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:03:20,177 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:03:20,217 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:03:20,217 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:03:26,223 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:03:26,262 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:03:26,262 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:03:32,269 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:03:32,306 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:03:32,306 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:03:38,310 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:03:38,349 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:03:38,349 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:03:44,356 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:03:44,394 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:03:44,395 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:03:50,401 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:03:50,401 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:03:50,401 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:03:50,401 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:03:56,407 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:03:56,409 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:03:56,410 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:04:02,416 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:04:02,417 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:04:02,417 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:04:08,420 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:04:08,422 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:04:08,422 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:04:14,429 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:04:14,429 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:04:14,429 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:04:20,435 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:04:20,436 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:04:20,437 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:04:25,439 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:04:25,439 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:04:25,439 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:04:29,446 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:04:29,448 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:04:29,448 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:04:32,456 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:04:32,457 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:04:32,457 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:04:34,463 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:04:34,465 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:04:35,472 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:04:35,472 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:04:36,479 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:04:36,479 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:04:36,481 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:04:36,481 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:04:38,488 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:04:38,493 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:04:38,493 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:04:41,500 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:04:41,504 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:04:41,504 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:04:45,507 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:04:45,544 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:04:45,544 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:04:50,551 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:04:50,589 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:04:50,589 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:04:56,596 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:04:56,633 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:04:56,633 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:05:02,640 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:05:02,678 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:05:02,678 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:05:08,684 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:05:08,722 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:05:08,723 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:05:14,730 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:05:14,767 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:05:14,767 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:05:20,774 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:05:20,811 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:05:20,811 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:05:26,818 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:05:26,856 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:05:26,856 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:05:32,862 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:05:32,862 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:05:32,863 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:05:32,863 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:05:38,865 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:05:38,867 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:05:38,867 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:05:44,875 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:05:44,875 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:05:44,875 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:05:50,882 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:05:50,884 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:05:50,884 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:05:56,890 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:05:56,890 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:05:56,890 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:06:02,898 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:06:02,901 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:06:02,901 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:06:07,905 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:06:07,905 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:06:07,906 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:06:11,912 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:06:11,913 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:06:11,913 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:06:14,919 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:06:14,919 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:06:14,919 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:06:16,925 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:06:16,929 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:06:17,936 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:06:17,936 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:06:18,937 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:06:18,937 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:06:18,939 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:06:18,939 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:06:20,946 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:06:20,985 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:06:20,985 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:06:23,993 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:06:24,049 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:06:24,049 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:06:28,055 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:06:28,093 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:06:28,093 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:06:33,100 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:06:33,138 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:06:33,138 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:06:39,146 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:06:39,185 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:06:39,185 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:06:45,193 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:06:45,231 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:06:45,231 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:06:51,238 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:06:51,277 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:06:51,277 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:06:57,284 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:06:57,323 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:06:57,323 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:07:03,327 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:07:03,363 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:07:03,363 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:07:09,371 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:07:09,408 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:07:09,409 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:07:15,416 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:07:15,416 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:07:15,416 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:07:15,416 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:07:21,418 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:07:21,420 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:07:21,420 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:07:27,426 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:07:27,427 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:07:27,427 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:07:33,434 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:07:33,435 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:07:33,436 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:07:39,442 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:07:39,442 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:07:39,442 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:07:45,449 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:07:45,451 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:07:45,452 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:07:50,458 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:07:50,459 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:07:50,459 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:07:54,465 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:07:54,467 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:07:54,467 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:07:57,473 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:07:57,473 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:07:57,473 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:07:59,480 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:07:59,482 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:08:00,488 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:08:00,489 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:08:01,495 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:08:01,495 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:08:01,497 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:08:01,498 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:08:03,504 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:08:03,543 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:08:03,543 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:08:06,550 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:08:06,588 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:08:06,589 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:08:10,590 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:08:10,629 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:08:10,629 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:08:15,635 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:08:15,674 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:08:15,675 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:08:21,682 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:08:21,721 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:08:21,721 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:08:27,728 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:08:27,758 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:08:27,758 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:08:33,766 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:08:33,804 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:08:33,804 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:08:39,810 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:08:39,848 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:08:39,848 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:08:45,855 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:08:45,893 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:08:45,893 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:08:51,900 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:08:51,937 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:08:51,937 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:08:57,945 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:08:57,945 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:08:57,945 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:08:57,945 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:09:03,953 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:09:03,955 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:09:03,955 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:09:09,962 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:09:09,962 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:09:09,963 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:09:15,970 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:09:15,972 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:09:15,972 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:09:21,976 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:09:21,977 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:09:21,977 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:09:27,985 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:09:27,987 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:09:27,987 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:09:32,994 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:09:32,994 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:09:32,994 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:09:37,001 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:09:37,003 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:09:37,003 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:09:40,009 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:09:40,009 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:09:40,009 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:09:42,011 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:09:42,013 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:09:43,018 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:09:43,019 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:09:44,025 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:09:44,025 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:09:44,027 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:09:44,028 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:09:46,034 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:09:46,073 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:09:46,073 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:09:49,080 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:09:49,119 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:09:49,119 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:09:53,126 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:09:53,166 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:09:53,166 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:09:58,173 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:09:58,211 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:09:58,211 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:10:04,218 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:10:04,255 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:10:04,255 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:10:10,262 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:10:10,299 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:10:10,300 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:10:16,308 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:10:16,346 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:10:16,346 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:10:22,354 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:10:22,392 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:10:22,392 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:10:28,399 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:10:28,437 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:10:28,437 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:10:34,445 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:10:34,482 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:10:34,482 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:10:40,489 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:10:40,490 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:10:40,490 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:10:40,490 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:10:46,497 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:10:46,497 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:10:46,498 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:10:52,504 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:10:52,504 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:10:52,504 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:10:58,511 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:10:58,512 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:10:58,512 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:11:04,520 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:11:04,520 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:11:04,520 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:11:10,528 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:11:10,528 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:11:10,528 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:11:15,533 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:11:15,533 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:11:15,533 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:11:19,540 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:11:19,540 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:11:19,540 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:11:22,548 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:11:22,548 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:11:22,548 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:11:24,555 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:11:24,555 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:11:25,561 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:11:25,561 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:11:26,568 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:11:26,568 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:11:26,570 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:11:26,570 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:11:28,576 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:11:28,578 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:11:28,578 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:11:31,585 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:11:31,587 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:11:31,588 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:11:35,596 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:11:35,598 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:11:35,599 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:11:40,605 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:11:40,606 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:11:40,607 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:11:46,614 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:11:46,616 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:11:46,616 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:11:52,624 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:11:52,625 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:11:52,626 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:11:58,633 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:11:58,635 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:11:58,636 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:12:04,643 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:12:04,645 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:12:04,645 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:12:10,652 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:12:10,654 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:12:10,654 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:12:16,661 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:12:16,663 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:12:16,664 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:12:22,673 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:12:22,673 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:12:22,673 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:12:22,673 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:12:28,677 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:12:28,677 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:12:28,678 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:12:34,683 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:12:34,683 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:12:34,683 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:12:40,691 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:12:40,692 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:12:40,692 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:12:46,694 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:12:46,694 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:12:46,694 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:12:52,702 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:12:52,702 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:12:52,702 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:12:57,709 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:12:57,709 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:12:57,709 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:13:01,716 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:13:01,716 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:13:01,716 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:13:04,723 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:13:04,723 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:13:04,723 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:13:06,730 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:13:06,730 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:13:07,737 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:13:07,737 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:13:08,743 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:13:08,743 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:13:08,745 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:13:08,745 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:13:10,752 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:13:10,754 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:13:10,755 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:13:13,774 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:13:13,777 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:13:13,777 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:13:17,784 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:13:17,785 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:13:17,786 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:13:22,791 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:13:22,793 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:13:22,794 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:13:28,797 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:13:28,800 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:13:28,800 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:13:34,806 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:13:34,808 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:13:34,808 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:13:40,814 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:13:40,816 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:13:40,817 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:13:46,823 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:13:46,825 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:13:46,825 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:13:52,832 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:13:52,834 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:13:52,834 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:13:58,841 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:13:58,843 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:13:58,844 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:14:04,850 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:14:04,850 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:14:04,850 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:14:04,850 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:14:10,853 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:14:10,853 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:14:10,853 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:14:16,861 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:14:16,861 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:14:16,861 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:14:22,868 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:14:22,868 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:14:22,868 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:14:28,874 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:14:28,875 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:14:28,875 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:14:34,881 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:14:34,882 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:14:34,882 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:14:39,889 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:14:39,889 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:14:39,889 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:14:43,894 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:14:43,894 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:14:43,894 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:14:46,900 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:14:46,901 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:14:46,901 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:14:48,909 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:14:48,909 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:14:49,915 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:14:49,916 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:14:50,921 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:14:50,922 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:14:50,924 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:14:50,924 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:14:52,932 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:14:52,934 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:14:52,934 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:14:55,942 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:14:55,944 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:14:55,944 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:14:59,952 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:14:59,954 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:14:59,954 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:15:04,960 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:15:04,962 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:15:04,962 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:15:10,969 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:15:10,970 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:15:10,970 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:15:16,977 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:15:16,978 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:15:16,979 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:15:22,986 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:15:22,988 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:15:22,988 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:15:28,996 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:15:28,999 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:15:28,999 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:15:35,005 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:15:35,007 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:15:35,007 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:15:41,015 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:15:41,016 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:15:41,016 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:15:47,023 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:15:47,023 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:15:47,023 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:15:47,024 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:15:53,029 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:15:53,030 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:15:53,030 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:15:59,037 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:15:59,037 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:15:59,037 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:16:05,045 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:16:05,045 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:16:05,045 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:16:11,053 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:16:11,053 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:16:11,053 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:16:17,060 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:16:17,060 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:16:17,060 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:16:22,068 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:16:22,068 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:16:22,068 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:16:26,071 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:16:26,071 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:16:26,072 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:16:29,078 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:16:29,078 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:16:29,078 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:16:31,084 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:16:31,084 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:16:32,091 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:16:32,091 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:16:33,097 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:16:33,097 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:16:33,099 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:16:33,099 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:16:35,100 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:16:35,102 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:16:35,102 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:16:38,109 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:16:38,112 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:16:38,112 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:16:42,118 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:16:42,120 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:16:42,120 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:16:47,123 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:16:47,125 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:16:47,125 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:16:53,131 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:16:53,134 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:16:53,134 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:16:59,138 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:16:59,140 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:16:59,140 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:17:05,147 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:17:05,148 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:17:05,148 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:17:11,155 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:17:11,157 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:17:11,157 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:17:17,164 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:17:17,165 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:17:17,165 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:17:23,173 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:17:23,176 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:17:23,176 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:17:29,184 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:17:29,184 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:17:29,184 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:17:29,184 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:17:35,191 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:17:35,191 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:17:35,192 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:17:41,198 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:17:41,198 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:17:41,198 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:17:47,201 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:17:47,201 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:17:47,201 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:17:53,208 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:17:53,208 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:17:53,208 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:17:59,215 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:17:59,216 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:17:59,216 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:18:04,223 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:18:04,223 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:18:04,223 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:18:08,230 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:18:08,230 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:18:08,230 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:18:11,236 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:18:11,237 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:18:11,237 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:18:13,242 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:18:13,242 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:18:14,248 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:18:14,248 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:18:15,255 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:18:15,255 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:18:15,257 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:18:15,257 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:18:17,262 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:18:17,263 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:18:17,264 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:18:20,265 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:18:20,266 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:18:20,267 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:18:24,274 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:18:24,276 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:18:24,276 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:18:29,283 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:18:29,285 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:18:29,285 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:18:35,330 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:18:35,331 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:18:35,332 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:18:41,338 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:18:41,340 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:18:41,341 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:18:47,348 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:18:47,350 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:18:47,351 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:18:53,358 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:18:53,360 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:18:53,360 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:18:59,367 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:18:59,370 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:18:59,370 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:19:05,378 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:19:05,379 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:19:05,379 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:19:11,386 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:19:11,387 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:19:11,387 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:19:11,387 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:19:17,395 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:19:17,395 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:19:17,395 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:19:23,401 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:19:23,401 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:19:23,401 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:19:29,408 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:19:29,408 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:19:29,409 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:19:35,417 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:19:35,417 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:19:35,417 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:19:41,421 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:19:41,421 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:19:41,421 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:19:46,426 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:19:46,426 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:19:46,426 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:19:50,434 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:19:50,434 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:19:50,435 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:19:53,443 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:19:53,443 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:19:53,443 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:19:55,449 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:19:55,449 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:19:56,454 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:19:56,455 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:19:57,461 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:19:57,461 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:19:57,463 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:19:57,463 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:19:59,471 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:19:59,473 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:19:59,473 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:20:02,480 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:20:02,482 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:20:02,482 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:20:06,490 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:20:06,492 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:20:06,493 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:20:11,500 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:20:11,502 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:20:11,502 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:20:17,510 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:20:17,512 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:20:17,512 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:20:23,575 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:20:23,577 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:20:23,577 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:20:29,667 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:20:29,670 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:20:29,670 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:20:35,676 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:20:35,679 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:20:35,679 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:20:41,686 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:20:41,687 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:20:41,687 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:20:47,695 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:20:47,697 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:20:47,697 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:20:53,704 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:20:53,704 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:20:53,704 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:20:53,705 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:20:59,712 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:20:59,712 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:20:59,712 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:21:05,718 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:21:05,718 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:21:05,718 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:21:11,723 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:21:11,723 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:21:11,723 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:21:17,730 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:21:17,730 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:21:17,730 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:21:23,738 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:21:23,738 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:21:23,738 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:21:28,744 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:21:28,744 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:21:28,744 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:21:32,750 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:21:32,750 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:21:32,751 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:21:35,758 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:21:35,758 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:21:35,758 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:21:37,765 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:21:37,766 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:21:38,772 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:21:38,772 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:21:39,776 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:21:39,776 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:21:39,778 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:21:39,779 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:21:41,785 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:21:41,787 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:21:41,787 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:21:44,793 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:21:44,795 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:21:44,795 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:21:48,803 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:21:48,805 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:21:48,805 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:21:53,813 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:21:53,815 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:21:53,815 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:21:59,822 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:21:59,824 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:21:59,824 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:22:05,830 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:22:05,831 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:22:05,831 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:22:11,839 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:22:11,841 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:22:11,841 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:22:17,849 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:22:17,851 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:22:17,851 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:22:23,857 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:22:23,859 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:22:23,859 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:22:29,866 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:22:29,867 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:22:29,867 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:22:35,874 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:22:35,874 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:22:35,874 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:22:35,874 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:22:41,881 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:22:41,881 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:22:41,882 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:22:47,889 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:22:47,889 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:22:47,889 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:22:53,897 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:22:53,897 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:22:53,897 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:22:59,905 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:22:59,905 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:22:59,905 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:23:05,912 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:23:05,912 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:23:05,912 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:23:10,920 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:23:10,920 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:23:10,920 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:23:14,927 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:23:14,928 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:23:14,928 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:23:17,936 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:23:17,936 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:23:17,936 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:23:19,942 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:23:19,942 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:23:20,948 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:23:20,948 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:23:21,954 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:23:21,954 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:23:21,957 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:23:21,957 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:23:23,964 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:23:23,965 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:23:23,966 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:23:26,973 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:23:26,975 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:23:26,975 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:23:30,982 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:23:30,984 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:23:30,984 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:23:35,991 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:23:35,993 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:23:35,993 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:23:42,000 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:23:42,002 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:23:42,003 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:23:48,009 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:23:48,011 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:23:48,011 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:23:54,017 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:23:54,018 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:23:54,018 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:24:00,024 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:24:00,025 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:24:00,025 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:24:06,032 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:24:06,034 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:24:06,034 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:24:12,041 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:24:12,042 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:24:12,042 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:24:18,048 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:24:18,048 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:24:18,048 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:24:18,048 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:24:24,051 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:24:24,052 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:24:24,052 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:24:30,059 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:24:30,059 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:24:30,059 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:24:36,061 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:24:36,061 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:24:36,061 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:24:42,069 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:24:42,069 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:24:42,069 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:24:48,071 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:24:48,072 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:24:48,072 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:24:53,080 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:24:53,080 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:24:53,080 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:24:57,087 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:24:57,088 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:24:57,088 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:25:00,094 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:25:00,094 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:25:00,094 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:25:02,102 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:25:02,102 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:25:03,109 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:25:03,109 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:25:04,116 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:25:04,116 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:25:04,118 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:25:04,118 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:25:06,125 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:25:06,127 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:25:06,127 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:25:09,131 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:25:09,133 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:25:09,134 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:25:13,141 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:25:13,143 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:25:13,144 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:25:18,150 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:25:18,152 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:25:18,152 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:25:24,160 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:25:24,162 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:25:24,163 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:25:30,169 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:25:30,171 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:25:30,171 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:25:36,177 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:25:36,179 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:25:36,179 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:25:42,185 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:25:42,188 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:25:42,188 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:25:48,194 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:25:48,196 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:25:48,196 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:25:54,203 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:25:54,205 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:25:54,205 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:26:00,212 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:26:00,213 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:26:00,213 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:26:00,213 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:26:06,219 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:26:06,219 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:26:06,220 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:26:12,226 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:26:12,226 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:26:12,226 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:26:18,266 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:26:18,267 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:26:18,267 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:26:24,269 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:26:24,270 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:26:24,270 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:26:30,275 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:26:30,275 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:26:30,275 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:26:35,278 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:26:35,278 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:26:35,278 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:26:39,286 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:26:39,286 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:26:39,286 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:26:42,292 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:26:42,292 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:26:42,292 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:26:44,299 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:26:44,299 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:26:45,305 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:26:45,306 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:26:46,312 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:26:46,312 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:26:46,314 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:26:46,314 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:26:48,328 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:26:48,329 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:26:48,330 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:26:51,338 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:26:51,340 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:26:51,340 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:26:55,347 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:26:55,349 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:26:55,349 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:27:00,356 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:27:00,357 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:27:00,358 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:27:06,365 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:27:06,367 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:27:06,367 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:27:12,374 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:27:12,376 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:27:12,376 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:27:18,383 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:27:18,384 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:27:18,384 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:27:24,390 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:27:24,392 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:27:24,393 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:27:30,400 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:27:30,401 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:27:30,402 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:27:36,422 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:27:36,424 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:27:36,424 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:27:42,431 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:27:42,431 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:27:42,431 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:27:42,432 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:27:48,439 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:27:48,439 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:27:48,440 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:27:54,446 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:27:54,446 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:27:54,446 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:28:00,453 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:28:00,453 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:28:00,453 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:28:06,456 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:28:06,456 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:28:06,456 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:28:12,463 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:28:12,463 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:28:12,463 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:28:17,470 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:28:17,471 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:28:17,471 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:28:21,477 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:28:21,477 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:28:21,477 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:28:24,484 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:28:24,484 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:28:24,484 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:28:26,492 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:28:26,492 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:28:27,499 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:28:27,499 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:28:28,506 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:28:28,506 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:28:28,508 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:28:28,508 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:28:30,515 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:28:30,517 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:28:30,518 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:28:33,525 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:28:33,527 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:28:33,527 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:28:37,534 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:28:37,536 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:28:37,536 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:28:42,543 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:28:42,545 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:28:42,545 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:28:48,553 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:28:48,555 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:28:48,555 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:28:54,563 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:28:54,565 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:28:54,565 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:29:00,572 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:29:00,574 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:29:00,575 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:29:06,583 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:29:06,584 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:29:06,585 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:29:12,591 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:29:12,593 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:29:12,593 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:29:18,600 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:29:18,601 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:29:18,601 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:29:24,609 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:29:24,610 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:29:24,610 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:29:24,610 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:29:30,616 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:29:30,616 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:29:30,616 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:29:36,624 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:29:36,624 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:29:36,624 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:29:42,631 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:29:42,631 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:29:42,631 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:29:48,633 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:29:48,633 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:29:48,633 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:29:54,640 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:29:54,641 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:29:54,641 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:29:59,647 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:29:59,647 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:29:59,647 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:30:03,654 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:30:03,654 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:30:03,654 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:30:06,662 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:30:06,662 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:30:06,662 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:30:08,672 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:30:08,672 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:30:09,678 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:30:09,679 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:30:10,685 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:30:10,685 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:30:10,688 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:30:10,688 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:30:12,690 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:30:12,692 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:30:12,692 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:30:15,700 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:30:15,702 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:30:15,702 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:30:19,709 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:30:19,711 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:30:19,712 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:30:24,718 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:30:24,720 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:30:24,720 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:30:30,727 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:30:30,729 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:30:30,730 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:30:36,736 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:30:36,738 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:30:36,738 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:30:42,744 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:30:42,745 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:30:42,746 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:30:48,753 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:30:48,755 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:30:48,755 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:30:54,761 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:30:54,763 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:30:54,763 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:31:00,769 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:31:00,771 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:31:00,771 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:31:06,778 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:31:06,778 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:31:06,778 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:31:06,778 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:31:12,785 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:31:12,786 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:31:12,786 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:31:18,793 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:31:18,793 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:31:18,793 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:31:24,796 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:31:24,796 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:31:24,797 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:31:30,803 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:31:30,804 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:31:30,804 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:31:36,811 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:31:36,811 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:31:36,811 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:31:41,818 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:31:41,819 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:31:41,819 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:31:45,826 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:31:45,826 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:31:45,827 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:31:48,834 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:31:48,834 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:31:48,835 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:31:50,842 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:31:50,842 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:31:51,849 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:31:51,849 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:31:52,855 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:31:52,855 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:31:52,857 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:31:52,858 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:31:54,860 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:31:54,862 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:31:54,862 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:31:57,870 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:31:57,872 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:31:57,872 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:32:01,878 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:32:01,880 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:32:01,880 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:32:06,885 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:32:06,887 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:32:06,887 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:32:12,894 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:32:12,896 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:32:12,896 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:32:18,903 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:32:18,905 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:32:18,905 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:32:24,913 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:32:24,915 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:32:24,915 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:32:30,922 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:32:30,924 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:32:30,924 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:32:36,931 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:32:36,932 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:32:36,932 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:32:42,939 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:32:42,941 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:32:42,941 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:32:48,947 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:32:48,947 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:32:48,947 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:32:48,947 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:32:54,951 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:32:54,951 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:32:54,951 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:33:00,958 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:33:00,958 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:33:00,958 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:33:06,960 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:33:06,960 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:33:06,960 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:33:12,967 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:33:12,967 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:33:12,968 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:33:18,974 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:33:18,974 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:33:18,974 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:33:23,982 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:33:23,982 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:33:23,982 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:33:27,989 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:33:27,990 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:33:27,990 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:33:30,998 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:33:30,998 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:33:30,998 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:33:33,005 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:33:33,005 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:33:34,011 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:33:34,012 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:33:35,018 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:33:35,018 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:33:35,019 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:33:35,019 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:33:37,026 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:33:37,028 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:33:37,029 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:33:40,035 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:33:40,038 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:33:40,038 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:33:44,040 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:33:44,041 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:33:44,042 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:33:49,047 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:33:49,049 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:33:49,049 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:33:55,057 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:33:55,059 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:33:55,060 [INFO] [CPU] Occupy core for 5s (Level 6)

Session terminated, killing shell... ...killed.
Terminated
cspag5955@b1-lab:~$ 
Connection to 127.0.0.1 closed.
cspag5955@c5r5s1 ~ % 
  [Restored May 24, 2026 at 2:49:14 PM]
Last login: Sun May 24 14:49:10 on console
cspag5955@c5r5s1 ~ % 
