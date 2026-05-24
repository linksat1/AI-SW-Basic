
Last login: Sat May 23 21:33:52 on ttys010
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ cd ~/AI-SW-Basic
cspag5955@b1-lab:~/AI-SW-Basic$ history > terminal-history-final.txt
cspag5955@b1-lab:~/AI-SW-Basic$ git add .
cspag5955@b1-lab:~/AI-SW-Basic$ git commit -m "docs: agent-app 실행 완료"
[pagchuseon-0523 79e9d96] docs: agent-app 실행 완료
 2 files changed, 1000 insertions(+), 486 deletions(-)
 create mode 100644 terminal-history-final.txt
 rewrite terminal-history.txt (100%)
cspag5955@b1-lab:~/AI-SW-Basic$ git push mine main
remote: Repository not found.
fatal: repository 'https://github.com/pagchuseon/AI-SW-Basic_3.git/' not found
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ git push mine main
remote: Repository not found.
fatal: repository 'https://github.com/pagchuseon/AI-SW-Basic_3.git/' not found
cspag5955@b1-lab:~/AI-SW-Basic$ git branch
  main
* pagchuseon-0523
  pagchuseon-work
cspag5955@b1-lab:~/AI-SW-Basic$ git push mine pagchuseon-0523
remote: Repository not found.
fatal: repository 'https://github.com/pagchuseon/AI-SW-Basic_3.git/' not found
cspag5955@b1-lab:~/AI-SW-Basic$ git remote -v
mine	https://pagchuseon:GITHUB_TOKEN2_REMOVED@github.com/pagchuseon/AI-SW-Basic_3.git (fetch)
mine	https://pagchuseon:GITHUB_TOKEN2_REMOVED@github.com/pagchuseon/AI-SW-Basic_3.git (push)
origin	https://linksat1:GITHUB_TOKEN_REMOVED@github.com/linksat1/AI-SW-Basic.git (fetch)
origin	https://linksat1:GITHUB_TOKEN_REMOVED@github.com/linksat1/AI-SW-Basic.git (push)
cspag5955@b1-lab:~/AI-SW-Basic$ history > ~/AI-SW-Basic/terminal-history-final.txt
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ cat >> /home/agent-admin/.bashrc << 'EOF'
> export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
EOF
-bash: /home/agent-admin/.bashrc: Permission denied
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ 
cspag5955@b1-lab:~/AI-SW-Basic$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ cat >> /home/agent-admin/.bashrc << 'EOF'
> export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
EOF
agent-admin@b1-lab:~$ source /home/agent-admin/.bashrc
agent-admin@b1-lab:~$ echo $AGENT_HOME
echo $AGENT_PORT
echo $AGENT_KEY_PATH
/home/agent-admin/agent-app
15034
/home/agent-admin/agent-app/api_keys/t_secret.key
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ python3 --version
Python 3.10.12
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ python3 agent_app.py
python3: can't open file '/home/agent-admin/agent-app/agent_app.py': [Errno 2] No such file or directory
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ cd /home/agent-admin/agent-app
python3 agent_app.py
python3: can't open file '/home/agent-admin/agent-app/agent_app.py': [Errno 2] No such file or directory
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export AGENT_LOG_DIR=/var/log/agent-app

./agent-app-linux-x86
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/5] Checking Port Availability          [FAIL]
   >>> Port 15034 is already in use.
[5/5] Verifying Log Permission            [FAIL]
   >>> Skipped due to previous critical failure.
--------------------------------------------------
System Boot Failed. Process Terminated.
agent-admin@b1-lab:~/agent-app$ 
  [Restored May 24, 2026 at 2:49:14 PM]
Last login: Sun May 24 14:49:14 on ttys007
Restored session: Sat May 23 23:02:21 KST 2026
cspag5955@c5r5s1 ~ % sudo ss -tulnp | grep 15034
Password:
Sorry, try again.
Password:
Sorry, try again.
Password:
sudo: 3 incorrect password attempts
cspag5955@c5r5s1 ~ % sudo ss -tulnp | grep 15034
Password:
Sorry, try again.
Password:
cspag5955 is not in the sudoers file.
This incident has been reported to the administrator.
cspag5955@c5r5s1 ~ % 
cspag5955@c5r5s1 ~ % 
cspag5955@c5r5s1 ~ % 
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ sudo ss -tulnp | grep 15034
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-admin
cd /home/agent-admin/agent-app
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export AGENT_LOG_DIR=/var/log/agent-app
./agent-app-linux-x86
Password: 
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ export AGENT_HOME=/home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ export AGENT_PORT=15034
agent-admin@b1-lab:~/agent-app$ export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
agent-admin@b1-lab:~/agent-app$ export AGENT_KEY_PATH=$AGENT_HOME/api_keys
agent-admin@b1-lab:~/agent-app$ export AGENT_LOG_DIR=/var/log/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86
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
2026-05-24 15:31:59,870 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-05-24 15:31:59,871 [INFO] Agent listening at port 15034
2026-05-24 15:31:59,871 [INFO] === Agent Worker Started ===
2026-05-24 15:31:59,871 [INFO]    > Cycle: 0 -> 256MB/Lv10 -> 0
2026-05-24 15:31:59,871 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 15:31:59,908 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 15:31:59,909 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:32:01,915 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 15:32:01,955 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 15:32:01,955 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:32:04,964 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 15:32:05,003 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 15:32:05,003 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:32:09,010 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 15:32:09,049 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 15:32:09,049 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:32:14,057 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 15:32:14,096 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 15:32:14,096 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:32:20,105 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 15:32:20,143 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 15:32:20,144 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:32:26,152 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 15:32:26,192 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 15:32:26,192 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:32:32,204 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 15:32:32,243 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 15:32:32,243 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:32:38,252 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 15:32:38,291 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 15:32:38,291 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:32:44,300 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 15:32:44,338 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 15:32:44,338 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:32:50,346 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 15:32:50,386 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 15:32:50,386 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:32:56,393 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 15:32:56,394 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 15:32:56,395 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 15:32:56,395 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:33:02,405 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 15:33:02,406 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 15:33:02,407 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:33:08,414 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 15:33:08,415 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 15:33:08,416 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:33:14,422 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 15:33:14,425 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 15:33:14,425 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:33:20,434 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 15:33:20,435 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 15:33:20,435 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:33:26,445 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 15:33:26,446 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 15:33:26,446 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:33:31,454 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 15:33:31,455 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 15:33:31,455 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:33:35,462 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 15:33:35,463 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 15:33:35,463 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:33:38,471 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 15:33:38,472 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 15:33:38,472 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:33:40,479 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 15:33:40,480 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 15:33:41,486 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 15:33:41,488 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 15:33:42,495 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 15:33:42,495 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 15:33:42,506 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 15:33:42,506 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:33:44,514 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 15:33:44,529 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 15:33:44,529 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:33:47,537 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 15:33:47,576 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 15:33:47,576 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:33:51,584 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 15:33:51,623 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 15:33:51,623 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:33:56,632 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 15:33:56,670 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 15:33:56,671 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:34:02,679 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 15:34:02,718 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 15:34:02,718 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:34:08,725 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 15:34:08,763 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 15:34:08,763 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:34:14,780 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 15:34:14,819 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 15:34:14,819 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:34:20,826 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 15:34:20,865 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 15:34:20,865 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:34:26,873 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 15:34:26,911 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 15:34:26,912 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:34:32,918 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 15:34:32,957 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 15:34:32,957 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:34:38,966 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 15:34:38,966 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 15:34:38,966 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 15:34:38,966 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:34:44,974 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 15:34:44,976 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 15:34:44,976 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:34:50,984 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 15:34:50,984 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 15:34:50,984 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:34:56,993 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 15:34:56,995 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 15:34:56,995 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:35:03,002 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 15:35:03,002 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 15:35:03,002 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:35:09,010 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 15:35:09,012 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 15:35:09,012 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:35:14,025 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 15:35:14,025 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 15:35:14,026 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:35:18,034 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 15:35:18,036 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 15:35:18,036 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:35:21,043 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 15:35:21,043 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 15:35:21,044 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:35:23,051 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 15:35:23,053 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 15:35:24,059 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 15:35:24,059 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 15:35:25,066 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 15:35:25,067 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 15:35:25,069 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 15:35:25,069 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:35:27,076 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 15:35:27,114 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 15:35:27,114 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:35:30,121 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 15:35:30,162 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 15:35:30,162 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:35:34,170 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 15:35:34,210 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 15:35:34,210 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:35:39,218 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 15:35:39,255 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 15:35:39,255 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:35:45,263 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 15:35:45,301 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 15:35:45,302 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:35:51,310 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 15:35:51,348 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 15:35:51,349 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:35:57,357 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 15:35:57,397 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 15:35:57,397 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:36:03,405 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 15:36:03,443 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 15:36:03,443 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:36:09,450 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 15:36:09,489 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 15:36:09,489 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:36:15,499 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 15:36:15,537 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 15:36:15,537 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:36:21,544 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 15:36:21,544 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 15:36:21,544 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 15:36:21,544 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:36:27,551 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 15:36:27,554 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 15:36:27,554 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:36:33,562 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 15:36:33,562 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 15:36:33,562 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:36:39,570 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 15:36:39,572 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 15:36:39,573 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:36:45,581 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 15:36:45,581 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 15:36:45,581 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:36:51,587 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 15:36:51,589 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 15:36:51,589 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:36:56,597 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 15:36:56,598 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 15:36:56,598 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:37:00,605 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 15:37:00,607 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 15:37:00,607 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:37:03,615 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 15:37:03,616 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 15:37:03,616 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:37:05,622 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 15:37:05,624 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 15:37:06,631 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 15:37:06,631 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 15:37:07,637 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 15:37:07,637 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 15:37:07,639 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 15:37:07,639 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:37:09,646 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 15:37:09,685 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 15:37:09,685 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:37:12,691 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 15:37:12,729 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 15:37:12,730 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:37:16,736 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 15:37:16,775 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 15:37:16,775 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:37:21,783 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 15:37:21,822 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 15:37:21,822 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:37:27,830 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 15:37:27,869 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 15:37:27,869 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:37:33,877 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 15:37:33,915 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 15:37:33,916 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:37:39,922 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 15:37:39,960 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 15:37:39,961 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:37:45,967 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 15:37:46,007 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 15:37:46,008 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:37:52,014 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 15:37:52,053 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 15:37:52,054 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:37:58,060 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 15:37:58,099 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 15:37:58,099 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 15:38:04,106 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 15:38:04,106 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 15:38:04,106 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 15:38:04,106 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 15:38:10,114 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 15:38:10,116 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 15:38:10,116 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:38:16,124 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 15:38:16,124 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 15:38:16,125 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:38:22,133 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 15:38:22,134 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 15:38:22,134 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:38:28,141 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 15:38:28,141 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 15:38:28,141 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:38:34,149 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 15:38:34,152 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 15:38:34,152 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:38:39,160 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 15:38:39,160 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 15:38:39,160 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:38:43,168 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 15:38:43,170 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 15:38:43,170 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:38:46,178 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 15:38:46,178 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 15:38:46,178 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:38:48,185 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 15:38:48,187 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 15:38:49,194 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 15:38:49,194 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 15:38:50,201 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 15:38:50,201 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 15:38:50,203 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 15:38:50,203 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 15:38:52,211 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 15:38:52,250 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 15:38:52,250 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 15:38:55,258 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 15:38:55,298 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 15:38:55,298 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 15:38:59,306 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 15:38:59,344 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 15:38:59,345 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 15:39:04,353 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 15:39:04,392 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 15:39:04,392 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 15:39:10,400 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 15:39:10,438 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 15:39:10,439 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 15:39:16,445 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 15:39:16,483 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 15:39:16,484 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 15:39:22,491 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 15:39:22,531 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 15:39:22,531 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 15:39:28,538 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 15:39:28,576 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 15:39:28,577 [INFO] [CPU] Occupy core for 5s (Level 9)
^C2026-05-24 15:39:32,641 [WARNING] Stop signal received. Terminating now...
2026-05-24 15:39:32,641 [INFO] === Agent Shutdown. Releasing resources. ===
2026-05-24 15:39:32,645 [INFO] User interrupted process. Shutting down gracefully...
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ mkdir -p /home/agent-admin/agent-app/bin
agent-admin@b1-lab:~/agent-app$ nano /home/agent-admin/agent-app/bin/monitor.sh
agent-admin@b1-lab:~/agent-app$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ mkdir -p /home/agent-admin/agent-app/bin
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app/bin
agent-admin@b1-lab:~/agent-app/bin$ nano monitor.sh
```
> ^C
agent-admin@b1-lab:~/agent-app/bin$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
[sudo] password for agent-admin: 
agent-admin is not in the sudoers file.  This incident will be reported.
agent-admin@b1-lab:~/agent-app/bin$ exit
logout
agent-admin@b1-lab:~/agent-app$ ls -l /home/agent-admin/agent-app/bin/monitor.sh
-rw-rw-r-- 1 agent-admin agent-admin 5260 May 24 15:55 /home/agent-admin/agent-app/bin/monitor.sh
agent-admin@b1-lab:~/agent-app$ ls /home/agent-admin/agent-app/
agent-app-linux-arm64  agent-app-linux-x86  api_keys  bin  __MACOSX  upload_files
agent-admin@b1-lab:~/agent-app$ ls /home/agent-admin/agent-app/bin/
monitor.sh
agent-admin@b1-lab:~/agent-app$ exit
logout
-bash: cd: /home/agent-admin/agent-app: Permission denied
-bash: ./agent-app-linux-x86: No such file or directory
cspag5955@b1-lab:~$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ ls -l /home/agent-admin/agent-app/bin/monitor.sh
ls: cannot access '/home/agent-admin/agent-app/bin/monitor.sh': Permission denied
cspag5955@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/
total 8
-rwxr-x--- 1 agent-dev agent-core 5260 May 24 15:55 monitor.sh
cspag5955@b1-lab:~$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
-rwxr-x--- 1 agent-dev agent-core 5260 May 24 15:55 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/
[sudo] password for agent-admin: 
agent-admin is not in the sudoers file.  This incident will be reported.
agent-admin@b1-lab:~$ exit
logout
cspag5955@b1-lab:~$ cspag5955@b1-lab:~$
-bash: cspag5955@b1-lab:~$: command not found
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/
total 8
-rwxr-x--- 1 agent-dev agent-core 5260 May 24 15:55 monitor.sh
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ source ~/.bashrc
agent-admin@b1-lab:~$ /home/agent-admin/agent-app/bin/monitor.sh
/home/agent-admin/agent-app/bin/monitor.sh: line 1: cspag5955@c5r5s1: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 2: cspag5955@b1-lab:~$: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 3: tcp: command not found

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~$ exit
logout
cspag5955@b1-lab:~$ sudo cat /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*  


#!/bin/bash
# =============================================================
# monitor.sh - 시스템 관제 자동화 스크립트
# 소유자: agent-dev / 그룹: agent-core / 권한: 750
# =============================================================

# ---- 설정 ----
APP_PROCESS="agent_app.py"      # 감시할 프로세스 이름
APP_PORT=15034                   # 감시할 포트 번호
LOG_FILE="/var/log/agent-app/monitor.log"  # 로그 파일 경로
MAX_LOG_SIZE=$((10 * 1024 * 1024))          # 최대 로그 크기: 10MB
MAX_LOG_FILES=10                             # 최대 로그 파일 개수

# 임계값
CPU_THRESHOLD=20
MEM_THRESHOLD=10
DISK_THRESHOLD=80

# ---- 로그 로테이션 함수 ----
rotate_log() {
    if [ -f "$LOG_FILE" ]; then
        local size
        size=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ "$size" -ge "$MAX_LOG_SIZE" ]; then
            # 기존 백업 파일들을 순서대로 밀어내기
            for i in $(seq $((MAX_LOG_FILES - 1)) -1 1); do
                [ -f "${LOG_FILE}.$i" ] && mv "${LOG_FILE}.$i" "${LOG_FILE}.$((i + 1))"
            done
            mv "$LOG_FILE" "${LOG_FILE}.1"
            touch "$LOG_FILE"
        fi
    fi
}

# ---- 현재 시각 ----
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""

# ============================================================
# [1] HEALTH CHECK - 프로세스 및 포트 확인
# ============================================================
echo "[HEALTH CHECK]"

# 프로세스 확인
PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    exit 1
else
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
fi

# 포트 확인
PORT_STATUS=$(ss -tulnp 2>/dev/null | grep ":${APP_PORT} ")
if [ -z "$PORT_STATUS" ]; then
    echo "Checking port $APP_PORT... [FAIL] Port not listening!"
    exit 1
else
    echo "Checking port $APP_PORT... [OK]"
fi

echo ""

# ============================================================
# [2] 방화벽 상태 점검 (경고만, 종료 안 함)
# ============================================================
echo "[FIREWALL CHECK]"

# UFW 상태 확인
if command -v ufw &>/dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | grep -i "Status:" | awk '{print $2}')
    if [ "$UFW_STATUS" = "active" ]; then
        echo "Firewall (UFW)... [OK] Active"
    else
        echo "[WARNING] Firewall (UFW) is not active!"
    fi
elif command -v firewall-cmd &>/dev/null; then
    FW_STATUS=$(sudo firewall-cmd --state 2>/dev/null)
    if [ "$FW_STATUS" = "running" ]; then
        echo "Firewall (firewalld)... [OK] Running"
    else
        echo "[WARNING] Firewall (firewalld) is not running!"
    fi
else
    echo "[WARNING] No firewall tool found (ufw/firewalld)!"
fi

echo ""

# ============================================================
# [3] RESOURCE MONITORING - CPU / MEM / DISK 수집
# ============================================================
echo "[RESOURCE MONITORING]"

# CPU 사용률 수집 (1초 간격 측정)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
# top 출력 형식에 따라 다를 수 있으므로 소수점 처리
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")

# 메모리 사용률 수집
MEM_INFO=$(free | grep Mem)
MEM_TOTAL=$(echo "$MEM_INFO" | awk '{print $2}')
MEM_USED=$(echo "$MEM_INFO" | awk '{print $3}')
if [ "$MEM_TOTAL" -gt 0 ]; then
    MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEM_USAGE="0.0"
fi

# 디스크 사용률 수집 (루트 파티션 /)
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""

# ============================================================
# [4] 임계값 경고 출력
# ============================================================

# CPU 경고
CPU_INT=$(echo "$CPU_USAGE" | cut -d'.' -f1)
if [ "${CPU_INT:-0}" -gt "$CPU_THRESHOLD" ]; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
fi

# MEM 경고
MEM_INT=$(echo "$MEM_USAGE" | cut -d'.' -f1)
if [ "${MEM_INT:-0}" -gt "$MEM_THRESHOLD" ]; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
fi

# DISK 경고
if [ "${DISK_USAGE:-0}" -gt "$DISK_THRESHOLD" ]; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"
fi

echo ""
echo "===================================="

# ============================================================
# [5] 로그 기록
# ============================================================

# 로그 디렉토리가 없으면 생성 시도
if [ ! -d "$(dirname "$LOG_FILE")" ]; then
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null
fi

# 로그 로테이션 실행
rotate_log

# 로그 한 줄 기록
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```
cspag5955@b1-lab:~$ sudo ls -1 /home/agent-admin/agent-app/
__MACOSX
agent-app-linux-arm64
agent-app-linux-x86
api_keys
bin
upload_files
cspag5955@b1-lab:~$ su - agent-dev
Password: 
su: Authentication failure
cspag5955@b1-lab:~$ sudo passwd agent-dev
New password: 
Retype new password: 
passwd: password updated successfully
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-dev
Password: 
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64
-bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64
-bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
agent-dev@b1-lab:~$ exit
logout
cspag5955@b1-lab:~$ sudo ls -la /home/agent-admin/agent-app/
total 13712
drwxr-xr-x  1 agent-admin agent-admin     142 May 23 21:36 .
drwxr-x---  1 agent-admin agent-admin     110 May 24 15:41 ..
drwxr-xr-x  1 agent-admin agent-admin      88 May 23 21:36 __MACOSX
-rw-r--r--  1 agent-admin agent-admin 7537848 May 18 17:06 agent-app-linux-arm64
-rwxr-xr-x  1 agent-admin agent-admin 6498144 May 20 11:11 agent-app-linux-x86
drwxrwx---+ 1 agent-admin agent-admin      44 May 23 21:28 api_keys
drwxr-xr-x  1 agent-admin agent-admin      20 May 24 15:55 bin
drwxrwsr-x+ 1 agent-admin agent-admin       0 May 23 19:52 upload_files
cspag5955@b1-lab:~$ exit
logout
Connection to 127.0.0.1 closed.
cspag5955@c5r5s1 ~ % sudo ls -la /home/agent-admin/agent-app/agent-app-linux-arm64
Password:
Sorry, try again.
Password:
Sorry, try again.
Password:
sudo: 3 incorrect password attempts
cspag5955@c5r5s1 ~ % orb shell

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cspag5955@cspagubuntu:/Users/cspag5955$ exit
logout
cspag5955@c5r5s1 ~ % orb shell b1-lab

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

-bash: line 1: b1-lab: command not found
cspag5955@c5r5s1 ~ % orb list

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

NAME         STATE    DISTRO  VERSION   ARCH   SIZE      IP
----         -----    ------  -------   ----   ----      --
b1-lab       running  ubuntu  jammy     amd64  2.1 GB    192.168.139.64
cspagubuntu  running  ubuntu  questing  amd64  687.2 MB  192.168.139.91
cspag5955@c5r5s1 ~ % orb shell b1-lab

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

-bash: line 1: b1-lab: command not found
cspag5955@c5r5s1 ~ % orb update
OrbStack updater will open in a new window.
cspag5955@c5r5s1 ~ % ssh cspag5955@192.168.139.64
ssh: connect to host 192.168.139.64 port 22: Operation timed out
cspag5955@c5r5s1 ~ % orb run -m b1-lab bash

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cspag5955@b1-lab:/Users/cspag5955$ sudo ls -la /home/agent-admin/agent-app/agent-app-linux-arm64
-rw-r--r-- 1 agent-admin agent-admin 7537848 May 18 17:06 /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ sudo chmod 750 /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ su - agent-dev
Password: 
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64
-bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
agent-dev@b1-lab:~$ 
agent-dev@b1-lab:~$ 
agent-dev@b1-lab:~$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/agent-app-linux-arm64
[sudo] password for agent-dev: 
Sorry, try again.
[sudo] password for agent-dev: 
Sorry, try again.
[sudo] password for agent-dev: 
sudo: 3 incorrect password attempts
agent-dev@b1-lab:~$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/agent-app-linux-arm64
[sudo] password for agent-dev: 
agent-dev is not in the sudoers file.  This incident will be reported.
agent-dev@b1-lab:~$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ sudo chmod 750 /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ sudo ls -la /home/agent-admin/agent-app/agent-app-linux-arm64
-rwxr-x--- 1 agent-dev agent-core 7537848 May 18 17:06 /home/agent-admin/agent-app/agent-app-linux-arm64
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ su - agent-dev
Password: 
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64
-bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
agent-dev@b1-lab:~$ ps aux | grep agent_app.py
agent-d+    1081  0.0  0.0   9224  2552 pts/1    S+   18:21   0:00 grep --color=auto agent_app.py
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/bin/monitor.sh
-bash: /home/agent-admin/agent-app/bin/monitor.sh: Permission denied
agent-dev@b1-lab:~$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ sudo ls -la /home/agent-admin/
total 16
drwxr-x--- 1 agent-admin agent-admin  110 May 24 15:41 .
drwxr-xr-x 1 root        root          78 May 23 19:46 ..
-rw------- 1 agent-admin agent-admin 3756 May 24 16:56 .bash_history
-rw-r--r-- 1 agent-admin agent-admin  220 Jan  7  2022 .bash_logout
-rw-r--r-- 1 agent-admin agent-admin 3986 May 23 21:49 .bashrc
drwxrwxr-x 1 agent-admin agent-admin   10 May 24 15:41 .local
-rw-r--r-- 1 agent-admin agent-admin  807 Jan  7  2022 .profile
drwxr-xr-x 1 agent-admin agent-admin  142 May 23 21:36 agent-app
cspag5955@b1-lab:/Users/cspag5955$ sudo chown agent-admin:agent-core /home/agent-admin/agent-app
cspag5955@b1-lab:/Users/cspag5955$ sudo chmod 750 /home/agent-admin/agent-app
cspag5955@b1-lab:/Users/cspag5955$ groups agent-dev
agent-dev : agent-dev agent-common agent-core
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ su - agent-dev
Password: 
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64
-bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
agent-dev@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64 &
[1] 1112
agent-dev@b1-lab:~$ -bash: /home/agent-admin/agent-app/agent-app-linux-arm64: Permission denied
^C
[1]+  Exit 126                /home/agent-admin/agent-app/agent-app-linux-arm64
agent-dev@b1-lab:~$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ sudo chmod 750 /home/agent-admin
cspag5955@b1-lab:/Users/cspag5955$ sudo chown agent-admin:agent-core /home/agent-admin
cspag5955@b1-lab:/Users/cspag5955$ sudo ls -la /home/
total 0
drwxr-xr-x 1 root        root        78 May 23 19:46 .
drwxr-xr-x 1 root        root       208 May 23 21:34 ..
drwxr-x--- 1 agent-admin agent-core 110 May 24 15:41 agent-admin
drwxr-x--- 1 agent-dev   agent-dev   80 May 24 17:01 agent-dev
drwxr-x--- 1 agent-test  agent-test  54 May 23 19:46 agent-test
drwxr-x--- 1 cspag5955   cspag5955  326 May 24 17:01 cspag5955
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ source ~/.bashrc
agent-admin@b1-lab:~$ /home/agent-admin/agent-app/agent-app-linux-arm64 &
[1] 1148
agent-admin@b1-lab:~$ [qemu-arm64]: Could not open '/lib/ld-linux-aarch64.so.1': No such file or directory
^C
[1]+  Exit 255                /home/agent-admin/agent-app/agent-app-linux-arm64
agent-admin@b1-lab:~$ ps aux | grep agent_app
agent-a+    1151  0.0  0.0   9220  2664 pts/1    S+   18:27   0:00 grep --color=auto agent_app
agent-admin@b1-lab:~$ /home/agent-admin/agent-app/bin/monitor.sh
/home/agent-admin/agent-app/bin/monitor.sh: line 1: cspag5955@c5r5s1: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 2: cspag5955@b1-lab:~$: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 3: tcp: command not found

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ orb run -m b1-lab bash
dial unix /opt/orbstack-guest/run/hcontrol.sock: connect: permission denied
agent-admin@b1-lab:~$ ./agent-app-linux-x86 
-bash: ./agent-app-linux-x86: No such file or directory
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ ls
agent-app-linux-arm64  agent-app-linux-x86  api_keys  bin  __MACOSX  upload_files
agent-admin@b1-lab:~/agent-app$ source ~/.bashrc
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 &
[1] 1190
agent-admin@b1-lab:~/agent-app$ >>> Starting Agent Boot Sequence...
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
^C
[1]+  Exit 1                  ./agent-app-linux-x86
agent-admin@b1-lab:~/agent-app$ nano /home/agent-admin/.bashrc
agent-admin@b1-lab:~/agent-app$ source ~/.bashrc
agent-admin@b1-lab:~/agent-app$ echo $AGENT_KEY_PATH
/home/agent-admin/agent-app/api_keys/t_secret.key
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 &
[1] 1198
agent-admin@b1-lab:~/agent-app$ >>> Starting Agent Boot Sequence...
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
^C
[1]+  Exit 1                  ./agent-app-linux-x86
agent-admin@b1-lab:~/agent-app$ nano ~/.bashrc
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ source ~/.bashrc
agent-admin@b1-lab:~/agent-app$ echo $AGENT_KEY_PATH
/home/agent-admin/agent-app/api_keys
agent-admin@b1-lab:~/agent-app$ cat /home/agent-admin/agent-app/api_keys/t_secret.key
agent_api_key_test
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 &
[1] 1207
agent-admin@b1-lab:~/agent-app$ >>> Starting Agent Boot Sequence...
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
2026-05-24 18:46:32,055 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-05-24 18:46:32,055 [INFO] Agent listening at port 15034
2026-05-24 18:46:32,056 [INFO] === Agent Worker Started ===
2026-05-24 18:46:32,056 [INFO]    > Cycle: 0 -> 256MB/Lv10 -> 0
2026-05-24 18:46:32,056 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:46:32,092 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:46:32,093 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:46:34,100 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:46:34,140 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:46:34,140 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:46:37,148 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:46:37,187 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:46:37,187 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:46:41,194 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:46:41,232 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:46:41,232 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:46:46,240 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:46:46,279 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:46:46,279 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:46:52,286 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:46:52,325 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:46:52,325 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:46:58,333 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:46:58,371 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:46:58,371 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:47:04,379 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:47:04,417 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:47:04,417 [INFO] [CPU] Occupy core for 5s (Level 8)

agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:47:10,424 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:47:10,462 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:47:10,463 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:47:16,470 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:47:16,510 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:47:16,510 [INFO] [CPU] Occupy core for 5s (Level 10)

agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh
/home/agent-admin/agent-app/bin/monitor.sh: line 1: cspag5955@c5r5s1: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 2: cspag5955@b1-lab:~$: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 3: tcp: command not found

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:47:22,517 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:47:22,556 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:47:22,556 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:47:28,564 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:47:28,564 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:47:28,565 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:47:28,565 [INFO] [CPU] Occupy core for 5s (Level 9)

agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh
/home/agent-admin/agent-app/bin/monitor.sh: line 1: cspag5955@c5r5s1: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 2: cspag5955@b1-lab:~$: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 3: tcp: command not found

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:47:34,573 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:47:34,574 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:47:34,575 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:47:40,582 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:47:40,584 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:47:40,584 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:47:46,590 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:47:46,591 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:47:46,592 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:47:52,599 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:47:52,600 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:47:52,600 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:47:58,609 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:47:58,610 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:47:58,610 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:48:03,618 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:48:03,620 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:48:03,620 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:48:07,627 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:48:07,628 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:48:07,628 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:48:10,635 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:48:10,636 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:48:10,636 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:48:12,643 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:48:12,644 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:48:13,651 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:48:13,652 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:48:14,658 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:48:14,658 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:48:14,663 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:48:14,663 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:48:16,670 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:48:16,676 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:48:16,676 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:48:19,690 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:48:19,730 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:48:19,731 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:48:23,739 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:48:23,778 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:48:23,778 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:48:28,788 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:48:28,825 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:48:28,826 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:48:34,832 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:48:34,870 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:48:34,870 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:48:40,878 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:48:40,918 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:48:40,918 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:48:46,925 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:48:46,963 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:48:46,963 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:48:52,971 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:48:53,010 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:48:53,010 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:48:59,017 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:48:59,056 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:48:59,056 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:49:05,064 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:49:05,102 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:49:05,102 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:49:11,110 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:49:11,111 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:49:11,111 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:49:11,111 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:49:17,119 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:49:17,121 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:49:17,121 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:49:23,128 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:49:23,128 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:49:23,128 [INFO] [CPU] Occupy core for 5s (Level 7)

agent-admin@b1-lab:~/agent-app$ cat > /home/agent-admin/agent-app/bin/monitor.sh << 'EOF'
#!/bin/bash
APP_PROCESS="agent-app-linux-x86"
APP_PORT=15034
LOG_FILE="/var/log/agent-app/monitor.log"

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""
echo "[HEALTH CHECK]"

PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    exit 1
else
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
fi

PORT_STATUS=$(ss -tulnp 2>/dev/null | grep ":${APP_PORT} ")
if [ -z "$PORT_STATUS" ]; then
    echo "Checking port $APP_PORT... [FAIL] Port not listening!"
    exit 1
else
    echo "Checking port $APP_PORT... [OK]"
fi

echo ""
echo "[FIREWALL CHECK]"
UFW_STATUS=$(sudo ufw status 2>/dev/null | grep -i "Status:" | awk '{print $2}')
if [ "$UFW_STATUS" = "active" ]; then
    echo "Firewall (UFW)... [OK] Active"
else
    echo "[WARNING] Firewall (UFW) is not active!"
fi

echo ""
echo "[RESOURCE MONITORING]"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")
MEM_INFO=$(free | grep Mem)
MEM_TOTAL=$(echo "$MEM_INFO" | awk '{print $2}')
MEM_USED=$(echo "$MEM_INFO" | awk '{print $3}')
MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""
echo "===================================="

echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"
echo "[INFO] Log appended: $LOG_FILE"
EOF
-bash: /home/agent-admin/agent-app/bin/monitor.sh: Permission denied
agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:49:29,135 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:49:29,137 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:49:29,137 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:49:35,145 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:49:35,145 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:49:35,146 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:49:41,152 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:49:41,154 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:49:41,155 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:49:46,162 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:49:46,162 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:49:46,162 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:49:50,170 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:49:50,173 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:49:50,173 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:49:53,180 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:49:53,180 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:49:53,180 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:49:55,186 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:49:55,188 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:49:56,194 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:49:56,194 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:49:57,200 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:49:57,200 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:49:57,201 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:49:57,202 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:49:59,208 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:49:59,246 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:49:59,246 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:50:02,253 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:50:02,294 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:50:02,294 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:50:06,301 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:50:06,339 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:50:06,339 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:50:11,347 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:50:11,384 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:50:11,384 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:50:17,391 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:50:17,429 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:50:17,429 [INFO] [CPU] Occupy core for 5s (Level 6)

agent-admin@b1-lab:~/agent-app$ head -5 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*  


agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:50:23,435 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:50:23,472 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:50:23,472 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:50:29,478 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:50:29,515 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:50:29,515 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:50:35,522 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:50:35,558 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:50:35,559 [INFO] [CPU] Occupy core for 5s (Level 9)
^C
agent-admin@b1-lab:~/agent-app$ head -5 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*  


agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:50:41,565 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:50:41,601 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:50:41,602 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:50:47,608 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:50:47,644 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:50:47,644 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:50:53,651 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:50:53,652 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:50:53,652 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:50:53,652 [INFO] [CPU] Occupy core for 5s (Level 9)
^C
agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:50:59,660 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:50:59,662 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:50:59,662 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:51:05,668 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:51:05,669 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:51:05,669 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:51:11,675 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:51:11,677 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:51:11,677 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:51:17,685 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:51:17,685 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:51:17,686 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:51:23,693 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:51:23,695 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:51:23,695 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:51:28,702 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:51:28,702 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:51:28,702 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:51:32,709 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:51:32,711 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:51:32,712 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:51:35,719 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:51:35,720 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:51:35,720 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:51:37,728 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:51:37,730 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:51:38,735 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:51:38,736 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:51:39,743 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:51:39,743 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:51:39,745 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:51:39,745 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:51:41,753 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:51:41,792 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:51:41,792 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:51:44,798 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:51:44,837 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:51:44,837 [INFO] [CPU] Occupy core for 3s (Level 3)

agent-admin@b1-lab:~/agent-app$ head -5 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*  


agent-admin@b1-lab:~/agent-app$ 2026-05-24 18:51:48,846 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:51:48,884 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:51:48,884 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:51:53,891 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:51:53,930 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:51:53,931 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:51:59,939 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:51:59,978 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:51:59,978 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:52:05,986 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:52:06,024 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:52:06,024 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:52:12,032 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:52:12,072 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:52:12,072 [INFO] [CPU] Occupy core for 5s (Level 8)
head -5 /home/agent-admin/agent-app/bin/monitor.sh2026-05-24 18:52:18,079 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:52:18,118 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:52:18,118 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:52:24,125 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:52:24,165 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:52:24,165 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:52:30,173 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:52:30,212 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:52:30,212 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:52:36,220 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:52:36,221 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:52:36,221 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:52:36,221 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:52:42,230 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:52:42,232 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:52:42,232 [INFO] [CPU] Occupy core for 5s (Level 8)
                                head -5 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*  


agent-admin@b1-lab:~/agent-app$ e2026-05-24 18:52:48,240 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:52:48,241 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:52:48,241 [INFO] [CPU] Occupy core for 5s (Level 7)

-bash: e: command not found
agent-admin@b1-lab:~/agent-app$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:52:54,248 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:52:54,250 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:52:54,251 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:53:00,257 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:53:00,257 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:53:00,258 [INFO] [CPU] Occupy core for 5s (Level 5)

cspag5955@b1-lab:/Users/cspag5955$ sudo sed -i '1,3d' /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:53:06,265 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:53:06,267 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:53:06,268 [INFO] [CPU] Occupy core for 4s (Level 4)

cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:53:11,274 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:53:11,274 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:53:11,274 [INFO] [CPU] Occupy core for 3s (Level 3)
head -3 /home/agent-admin/agent-apphead -3 /home/agent-admin/agent-app/bin/monitor.sh
head: cannot open '/home/agent-admin/agent-app/bin/monitor.sh' for reading: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ head -3 /home/agent-admin/agent-app/bin/monitor.sh
head: cannot open '/home/agent-admin/agent-app/bin/monitor.sh' for reading: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:53:15,281 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:53:15,283 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:53:15,283 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:53:18,290 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:53:18,291 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:53:18,291 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:53:20,298 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:53:20,299 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:53:21,306 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:53:21,306 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:53:22,313 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:53:22,313 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:53:22,315 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:53:22,316 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:53:24,324 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:53:24,363 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:53:24,363 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:53:27,372 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:53:27,410 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:53:27,410 [INFO] [CPU] Occupy core for 3s (Level 3)

cspag5955@b1-lab:/Users/cspag5955$ head -3 /home/agent-admin/agent-app/bin/monitor.sh2026-05-24 18:53:31,417 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:53:31,454 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:53:31,454 [INFO] [CPU] Occupy core for 4s (Level 4)
                                   head -3 /home/agent-admin/agent-app/bin/monitor.sh
head: cannot open '/home/agent-admin/agent-app/bin/monitor.sh' for reading: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:53:36,461 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:53:36,499 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:53:36,499 [INFO] [CPU] Occupy core for 5s (Level 5)
head -3 /home/agent-admin/agent-apphead -3 /home/agent-admin/agent-app/bin/monitor.sh
head: cannot open '/home/agent-admin/agent-app/bin/monitor.sh' for reading: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ head -3 /home/agent-admin/agent-app/bin/monitor.sh
head: cannot open '/home/agent-admin/agent-app/bin/monitor.sh' for reading: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:53:42,506 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:53:42,544 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:53:42,544 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:53:48,551 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:53:48,589 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:53:48,589 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:53:54,596 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:53:54,634 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:53:54,634 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:54:00,657 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:54:00,695 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:54:00,695 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:54:06,703 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:54:06,740 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:54:06,740 [INFO] [CPU] Occupy core for 5s (Level 10)

cspag5955@b1-lab:/Users/cspag5955$ whoami
cspag5955
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:54:12,749 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:54:12,787 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:54:12,787 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:54:18,793 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:54:18,794 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:54:18,794 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:54:18,794 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:54:24,802 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:54:24,804 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:54:24,804 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:54:30,811 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:54:30,811 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:54:30,812 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:54:36,818 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:54:36,819 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:54:36,819 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:54:42,826 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:54:42,826 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:54:42,826 [INFO] [CPU] Occupy core for 5s (Level 5)

cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ sudo sed -i '1,3d' /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:54:48,832 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:54:48,834 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:54:48,834 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:54:53,841 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:54:53,841 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:54:53,841 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:54:57,849 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:54:57,851 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:54:57,851 [INFO] [CPU] Occupy core for 2s (Level 2)

cspag5955@b1-lab:/Users/cspag5955$ sudo head -3 /home/agent-admin/agent-app/bin/monitor.sh
# =============================================================
# monitor.sh - 시스템 관제 자동화 스크립트
# 소유자: agent-dev / 그룹: agent-core / 권한: 750
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:55:00,858 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:55:00,858 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:55:00,859 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:55:02,865 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:55:02,867 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:55:03,873 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:55:03,873 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:55:04,880 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:55:04,880 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:55:04,882 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:55:04,882 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:55:06,889 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:55:06,903 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:55:06,903 [INFO] [CPU] Occupy core for 2s (Level 2)

cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 2026-05-24 18:55:09,909 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:55:09,914 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:55:09,914 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:55:13,923 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:55:13,952 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:55:13,952 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:55:18,960 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:55:18,998 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:55:18,998 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:55:25,004 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:55:25,043 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:55:25,043 [INFO] [CPU] Occupy core for 5s (Level 6)

2026-05-24 18:55:31,044 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:55:31,066 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:55:31,066 [INFO] [CPU] Occupy core for 5s (Level 7)
su - agent-admin
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 
2026-05-24 18:55:37,073 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:55:37,087 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:55:37,088 [INFO] [CPU] Occupy core for 5s (Level 8)
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 2026-05-24 18:55:43,096 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:55:43,107 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:55:43,107 [INFO] [CPU] Occupy core for 5s (Level 9)

su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:55:49,114 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:55:49,151 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:55:49,152 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:55:55,159 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:55:55,197 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:55:55,197 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:56:01,205 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:56:01,206 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:56:01,206 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:56:01,206 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:56:07,213 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:56:07,214 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:56:07,214 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:56:13,222 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:56:13,223 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:56:13,223 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 18:56:19,231 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:56:19,233 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:56:19,233 [INFO] [CPU] Occupy core for 5s (Level 6)

cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:56:25,240 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:56:25,240 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:56:25,240 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:56:31,248 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:56:31,249 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:56:31,249 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:56:36,256 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:56:36,256 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:56:36,257 [INFO] [CPU] Occupy core for 3s (Level 3)

cspag5955@b1-lab:/Users/cspag5955$ source ~/.bashrc
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:56:40,264 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:56:40,265 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:56:40,266 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:56:43,272 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:56:43,273 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:56:43,273 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:56:45,281 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:56:45,283 [INFO] [Memory] Releasing... (-25MB) Total: 25MB

cspag5955@b1-lab:/Users/cspag5955$ /home/agent-admin/agent-app/bin/monitor.sh2026-05-24 18:56:46,289 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:56:46,289 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
                                   /home/agent-admin/agent-app/bin/monitor.sh
bash: /home/agent-admin/agent-app/bin/monitor.sh: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:56:47,296 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:56:47,296 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:56:47,298 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:56:47,299 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:56:49,307 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:56:49,345 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:56:49,345 [INFO] [CPU] Occupy core for 2s (Level 2)

cspag5955@b1-lab:/Users/cspag5955$ /home/agent-admin/agent-app/bin/monitor.sh
bash: /home/agent-admin/agent-app/bin/monitor.sh: Permission denied
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:56:52,353 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:56:52,391 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:56:52,392 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:56:56,397 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:56:56,436 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:56:56,437 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:57:01,444 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:57:01,482 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:57:01,483 [INFO] [CPU] Occupy core for 5s (Level 5)

cspag5955@b1-lab:/Users/cspag5955$ /home/agent-admin/agent-app/bin/monitor.sh 2>/dev/null
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:57:07,490 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:57:07,528 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:57:07,528 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:57:13,535 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:57:13,573 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:57:13,573 [INFO] [CPU] Occupy core for 5s (Level 7)

cspag5955@b1-lab:/Users/cspag5955$ source ~/.bashrc
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:57:19,580 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:57:19,618 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:57:19,618 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-24 18:57:25,625 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:57:25,663 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:57:25,663 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:57:31,670 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:57:31,708 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:57:31,708 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:57:37,716 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:57:37,755 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:57:37,756 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 18:57:43,762 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:57:43,763 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:57:43,763 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:57:43,763 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 18:57:49,770 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:57:49,772 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:57:49,772 [INFO] [CPU] Occupy core for 5s (Level 8)

cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 
2026-05-24 18:57:55,780 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:57:55,781 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:57:55,781 [INFO] [CPU] Occupy core for 5s (Level 7)
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:58:01,787 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:58:01,789 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:58:01,789 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:58:07,797 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:58:07,797 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:58:07,797 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:58:13,804 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:58:13,806 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:58:13,806 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:58:18,812 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 18:58:18,812 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 18:58:18,812 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:58:22,819 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 18:58:22,821 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 18:58:22,821 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:58:25,830 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 18:58:25,830 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 18:58:25,830 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:58:27,838 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 18:58:27,840 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 18:58:28,846 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 18:58:28,846 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 18:58:29,852 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 18:58:29,852 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 18:58:29,854 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 18:58:29,855 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 18:58:31,861 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 18:58:31,900 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 18:58:31,900 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 18:58:34,908 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-24 18:58:34,946 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-24 18:58:34,946 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 18:58:38,955 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-24 18:58:38,993 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-24 18:58:38,993 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 18:58:44,001 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-24 18:58:44,039 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-24 18:58:44,040 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:58:50,047 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-24 18:58:50,086 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-24 18:58:50,086 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:58:56,092 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-24 18:58:56,131 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-24 18:58:56,131 [INFO] [CPU] Occupy core for 5s (Level 7)

cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 2026-05-24 18:59:02,139 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-24 18:59:02,177 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-24 18:59:02,177 [INFO] [CPU] Occupy core for 5s (Level 8)

su - agent-admin
1232026-05-24 18:59:08,184 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 18:59:08,206 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 18:59:08,206 [INFO] [CPU] Occupy core for 5s (Level 9)
4
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 
2026-05-24 18:59:14,214 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 18:59:14,235 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 18:59:14,235 [INFO] [CPU] Occupy core for 5s (Level 10)
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 2026-05-24 18:59:20,243 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 18:59:20,263 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 18:59:20,263 [INFO] [CPU] Occupy core for 5s (Level 10)

su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:59:26,271 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 18:59:26,272 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 18:59:26,272 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 18:59:26,272 [INFO] [CPU] Occupy core for 5s (Level 9)

cspag5955@b1-lab:/Users/cspag5955$ su - agent-admin
Password: 
2026-05-24 18:59:32,277 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 18:59:32,279 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 18:59:32,279 [INFO] [CPU] Occupy core for 5s (Level 8)
su: Authentication failure
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:59:38,288 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 18:59:38,288 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 18:59:38,288 [INFO] [CPU] Occupy core for 5s (Level 7)

cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ 
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 18:59:44,296 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 18:59:44,298 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 18:59:44,298 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 18:59:50,306 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 18:59:50,307 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 18:59:50,307 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 18:59:56,314 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 18:59:56,316 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 18:59:56,316 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-24 19:00:01,322 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 19:00:01,323 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 19:00:01,323 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-24 19:00:05,385 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 19:00:05,386 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 19:00:05,386 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 19:00:08,392 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 19:00:08,392 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 19:00:08,393 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 19:00:10,399 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 19:00:10,401 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 19:00:11,407 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 19:00:11,407 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 19:00:12,415 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 19:00:12,415 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 19:00:12,417 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 19:00:12,417 [INFO] [CPU] Occupy core for 1s (Level 1)

cspag5955@b1-lab:/Users/cspag5955$ sudo passwd agent-admin2026-05-24 19:00:14,425 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 19:00:14,463 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 19:00:14,464 [INFO] [CPU] Occupy core for 2s (Level 2)
sudo passwd agent-admin
New password: 2026-05-24 19:00:17,470 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
                                                                                           2026-05-24 19:00:17,509 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
                                                                2026-05-24 19:00:17,509 [INFO] [CPU] Occupy core for 3s (Level 3)
                           2026-05-24 19:00:21,517 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
  2026-05-24 19:00:21,555 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
                                                                              2026-05-24 19:00:21,556 [INFO] [CPU] Occupy core for 4s (Level 4)
                                         2026-05-24 19:00:26,563 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
                 2026-05-24 19:00:26,602 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
                                                                                             2026-05-24 19:00:26,603 [INFO] [CPU] Occupy core for 5s (Level 5)
                                                        2026-05-24 19:00:32,610 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
                                2026-05-24 19:00:32,648 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
      2026-05-24 19:00:32,648 [INFO] [CPU] Occupy core for 5s (Level 6)
                                                                       2026-05-24 19:00:38,653 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
                                               2026-05-24 19:00:38,692 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
                     2026-05-24 19:00:38,692 [INFO] [CPU] Occupy core for 5s (Level 7)
                                                                                      2026-05-24 19:00:44,700 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
                                                              2026-05-24 19:00:44,738 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
                                    2026-05-24 19:00:44,738 [INFO] [CPU] Occupy core for 5s (Level 8)

Retype new password: 
Sorry, passwords do not match.
passwd: Authentication token manipulation error
passwd: password unchanged
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:00:50,745 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-24 19:00:50,783 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-24 19:00:50,784 [INFO] [CPU] Occupy core for 5s (Level 9)

cspag5955@b1-lab:/Users/cspag5955$ kill %1
bash: kill: %1: no such job
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:00:56,791 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-24 19:00:56,830 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-24 19:00:56,830 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-24 19:01:02,836 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-24 19:01:02,874 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-24 19:01:02,875 [INFO] [CPU] Occupy core for 5s (Level 10)

cspag5955@b1-lab:/Users/cspag5955$ [1]+  Terminated  ./agent-app-linux-x86
bash: [1]+: command not found
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:01:08,881 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-24 19:01:08,882 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-24 19:01:08,882 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-24 19:01:08,882 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-24 19:01:14,890 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-24 19:01:14,892 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-24 19:01:14,892 [INFO] [CPU] Occupy core for 5s (Level 8)

cspag5955@b1-lab:/Users/cspag5955$ kill %1
bash: kill: %1: no such job
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:01:20,899 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-24 19:01:20,899 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-24 19:01:20,899 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-24 19:01:26,907 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-24 19:01:26,908 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-24 19:01:26,908 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-24 19:01:32,914 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-24 19:01:32,914 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-24 19:01:32,914 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-24 19:01:38,923 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-24 19:01:38,925 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-24 19:01:38,925 [INFO] [CPU] Occupy core for 4s (Level 4)

cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:01:43,932 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-24 19:01:43,932 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-24 19:01:43,932 [INFO] [CPU] Occupy core for 3s (Level 3)
pgrep -f agent-app-linux-x86
1207
1208
cspag5955@b1-lab:/Users/cspag5955$ pgrep -f agent-app-linux-x86
1207
1208
cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:01:47,939 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-24 19:01:47,941 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-24 19:01:47,941 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-24 19:01:50,948 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-24 19:01:50,949 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-24 19:01:50,949 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-24 19:01:52,956 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-24 19:01:52,958 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-24 19:01:53,965 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-24 19:01:53,965 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-24 19:01:54,971 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-24 19:01:54,971 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-24 19:01:54,973 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-24 19:01:54,973 [INFO] [CPU] Occupy core for 1s (Level 1)

cspag5955@b1-lab:/Users/cspag5955$ 2026-05-24 19:01:56,980 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-24 19:01:56,987 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-24 19:01:56,987 [INFO] [CPU] Occupy core for 2s (Level 2)
sudo kill $(pgrep -f agent-app-linusudo kill $(pgrep -f agent-app-linux-x86)
cspag5955@b1-lab:/Users/cspag5955$ sudo kill $(pgrep -f agent-app-linux-x86)

Usage:
 kill [options] <pid> [...]

Options:
 <pid> [...]            send signal to every <pid> listed
 -<signal>, -s, --signal <signal>
                        specify the <signal> to be sent
 -q, --queue <value>    integer value to be sent with the signal
 -l, --list=[<signal>]  list all signal names, or convert one to a name
 -L, --table            list all signal names in a nice table

 -h, --help     display this help and exit
 -V, --version  output version information and exit

For more details see kill(1).
cspag5955@b1-lab:/Users/cspag5955$ pgrep -f agent-app-linux-x86
cspag5955@b1-lab:/Users/cspag5955$ sudo passwd agent-admin
New password: 
Retype new password: 
passwd: password updated successfully
cspag5955@b1-lab:/Users/cspag5955$ sudo su - agent-admin
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 > /dev/null 2>&1 &
[1] 1312
agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 > /dev/null 2>&1 &
[2] 1319
agent-admin@b1-lab:~/agent-app$ pgrep -f agent-app-linux-x86
1312
1313
[2]+  Exit 1                  ./agent-app-linux-x86 > /dev/null 2>&1
agent-admin@b1-lab:~/agent-app$ sed -i 's/APP_PROCESS="agent_app.py"/APP_PROCESS="agent-app-linux-x86"/' /home/agent-admin/agent-app/bin/monitor.sh
agent-admin@b1-lab:~/agent-app$ grep APP_PROCESS /home/agent-admin/agent-app/bin/monitor.sh
APP_PROCESS="agent-app-linux-x86"      # 감시할 프로세스 이름
PID=$(pgrep -f "$APP_PROCESS" | head -1)
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
agent-admin@b1-lab:~/agent-app$ APP_PROCESS="agent-app-linux-x86" ✅
-bash: ✅: command not found
agent-admin@b1-lab:~/agent-app$ APP_PROCESS="agent-app-linux-x86"
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 > /dev/null 2>&1 &
[2] 1325
agent-admin@b1-lab:~/agent-app$ pgrep -f agent-app-linux-x86
1312
1313
[2]+  Exit 1                  ./agent-app-linux-x86 > /dev/null 2>&1
agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh

1단계부터 실행 후 결과를 보여주세요! 😊

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1312)
Checking port 15034... [OK]

[FIREWALL CHECK]
[sudo] password for agent-admin: 
[WARNING] Firewall (UFW) is not active!

[RESOURCE MONITORING]
CPU Usage  : 0.0%
MEM Usage  : 3.7%
DISK Used  : 1%


====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
/home/agent-admin/agent-app/bin/monitor.sh: line 160: unexpected EOF while looking for matching ``'
/home/agent-admin/agent-app/bin/monitor.sh: line 161: syntax error: unexpected end of file
-bash: 1단계부터: command not found
agent-admin@b1-lab:~/agent-app$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ sudo ufw enable
Firewall is active and enabled on system startup
cspag5955@b1-lab:/Users/cspag5955$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere                  
15034/tcp                  ALLOW       Anywhere                  
20022/tcp (v6)             ALLOW       Anywhere (v6)             
15034/tcp (v6)             ALLOW       Anywhere (v6)             

cspag5955@b1-lab:/Users/cspag5955$ sudo tail -10 /home/agent-admin/agent-app/bin/monitor.sh
fi

# 로그 로테이션 실행
rotate_log

# 로그 한 줄 기록
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```
cspag5955@b1-lab:/Users/cspag5955$ sudo su - agent-admin
agent-admin@b1-lab:~$ source ~/.bashrc
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 > /dev/null 2>&1 &
[1] 1492
agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1312)
Checking port 15034... [OK]

[FIREWALL CHECK]
[sudo] password for agent-admin: 
[WARNING] Firewall (UFW) is not active!

[RESOURCE MONITORING]
CPU Usage  : 0.0%
MEM Usage  : 4.5%
DISK Used  : 1%


====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
/home/agent-admin/agent-app/bin/monitor.sh: line 160: unexpected EOF while looking for matching ``'
/home/agent-admin/agent-app/bin/monitor.sh: line 161: syntax error: unexpected end of file
[1]+  Exit 1                  ./agent-app-linux-x86 > /dev/null 2>&1
agent-admin@b1-lab:~/agent-app$ exit
logout
cspag5955@b1-lab:/Users/cspag5955$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere                  
15034/tcp                  ALLOW       Anywhere                  
20022/tcp (v6)             ALLOW       Anywhere (v6)             
15034/tcp (v6)             ALLOW       Anywhere (v6)             

cspag5955@b1-lab:/Users/cspag5955$ sudo tail -5 /home/agent-admin/agent-app/bin/monitor.sh
# 로그 한 줄 기록
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```
cspag5955@b1-lab:/Users/cspag5955$ sudo wc -l /home/agent-admin/agent-app/bin/monitor.sh
160 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:/Users/cspag5955$ sudo usermod -aG sudo agent-admin
cspag5955@b1-lab:/Users/cspag5955$ sudo tail -5 /home/agent-admin/agent-app/bin/monitor.sh
# 로그 한 줄 기록
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```
cspag5955@b1-lab:/Users/cspag5955$ sudo usermod -aG sudo agent-admin
cspag5955@b1-lab:/Users/cspag5955$ sudo su - agent-admin
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

agent-admin@b1-lab:~$ source ~/.bashrc
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86 > /dev/null 2>&1 &
[1] 1588
agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1312)
Checking port 15034... [OK]

[FIREWALL CHECK]
[sudo] password for agent-admin: 
Firewall (UFW)... [OK] Active

[RESOURCE MONITORING]
CPU Usage  : 0.0%
MEM Usage  : 4.0%
DISK Used  : 1%


====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
/home/agent-admin/agent-app/bin/monitor.sh: line 160: unexpected EOF while looking for matching ``'
/home/agent-admin/agent-app/bin/monitor.sh: line 161: syntax error: unexpected end of file
[1]+  Exit 1                  ./agent-app-linux-x86 > /dev/null 2>&1
agent-admin@b1-lab:~/agent-app$ sudo wc -l /home/agent-admin/agent-app/bin/monitor.sh
160 /home/agent-admin/agent-app/bin/monitor.sh
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ sudo sed -n '155,161p' /home/agent-admin/agent-app/bin/monitor.sh

# 로그 한 줄 기록
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```
agent-admin@b1-lab:~/agent-app$ /home/agent-admin/agent-app/bin/monitor.sh

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1312)
Checking port 15034... [OK]

[FIREWALL CHECK]
Firewall (UFW)... [OK] Active

[RESOURCE MONITORING]
CPU Usage  : 0.0%
MEM Usage  : 3.4%
DISK Used  : 1%


====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
/home/agent-admin/agent-app/bin/monitor.sh: line 160: unexpected EOF while looking for matching ``'
/home/agent-admin/agent-app/bin/monitor.sh: line 161: syntax error: unexpected end of file
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ 
agent-admin@b1-lab:~/agent-app$ sudo cat /var/log/agent-app/monitor.log
[2026-05-24 19:05:55] PID:1312 CPU:0.0% MEM:3.7% DISK_USED:1%
[2026-05-24 19:08:41] PID:1312 CPU:0.0% MEM:4.5% DISK_USED:1%
[2026-05-24 19:11:06] PID:1312 CPU:0.0% MEM:4.0% DISK_USED:1%
[2026-05-24 19:16:31] PID:1312 CPU:0.0% MEM:3.4% DISK_USED:1%
agent-admin@b1-lab:~/agent-app$ pwd
/home/agent-admin/agent-app
agent-admin@b1-lab:~/agent-app$ whoami
agent-admin
agent-admin@b1-lab:~/agent-app$ sudo su - agent-admin
[sudo] password for agent-admin: 
agent-admin@b1-lab:~$ pgrep -f agent-app-linux-x86
1312
1313
agent-admin@b1-lab:~$ crontab -e
no crontab for agent-admin - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny

Choose 1-3 [1]: 1
crontab: installing new crontab
agent-admin@b1-lab:~$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
agent-admin@b1-lab:~$ tail -f /var/log/agent-app/monitor.log
[2026-05-24 19:05:55] PID:1312 CPU:0.0% MEM:3.7% DISK_USED:1%
[2026-05-24 19:08:41] PID:1312 CPU:0.0% MEM:4.5% DISK_USED:1%
[2026-05-24 19:11:06] PID:1312 CPU:0.0% MEM:4.0% DISK_USED:1%
[2026-05-24 19:16:31] PID:1312 CPU:0.0% MEM:3.4% DISK_USED:1%
[2026-05-24 20:23:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:24:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:25:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:26:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%




  
^C
agent-admin@b1-lab:~$ orb list
dial unix /opt/orbstack-guest/run/hcontrol.sock: connect: permission denied
agent-admin@b1-lab:~$ pwd
/home/agent-admin
agent-admin@b1-lab:~$ who
cspag5955 pts/5        2026-05-24 19:10
agent-admin pts/6        2026-05-24 20:21
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ grep "^Port" /etc/ssh/sshd_config
Port 20022
agent-admin@b1-lab:~$ sudo ufw status
[sudo] password for agent-admin: 
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere                  
15034/tcp                  ALLOW       Anywhere                  
20022/tcp (v6)             ALLOW       Anywhere (v6)             
15034/tcp (v6)             ALLOW       Anywhere (v6)             

agent-admin@b1-lab:~$ id agent-admin && id agent-dev && id agent-test
uid=1000(agent-admin) gid=1002(agent-admin) groups=1002(agent-admin),27(sudo),1000(agent-common),1001(agent-core)
uid=1001(agent-dev) gid=1003(agent-dev) groups=1003(agent-dev),1000(agent-common),1001(agent-core)
uid=1002(agent-test) gid=1004(agent-test) groups=1004(agent-test),1000(agent-common)
agent-admin@b1-lab:~$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
agent-admin@b1-lab:~$ tail -20 /var/log/agent-app/monitor.log
[2026-05-24 19:05:55] PID:1312 CPU:0.0% MEM:3.7% DISK_USED:1%
[2026-05-24 19:08:41] PID:1312 CPU:0.0% MEM:4.5% DISK_USED:1%
[2026-05-24 19:11:06] PID:1312 CPU:0.0% MEM:4.0% DISK_USED:1%
[2026-05-24 19:16:31] PID:1312 CPU:0.0% MEM:3.4% DISK_USED:1%
[2026-05-24 20:23:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:24:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:25:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:26:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:27:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:28:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:29:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:30:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:31:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:32:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:33:01] PID:1312 CPU:1.1% MEM:4.8% DISK_USED:1%
agent-admin@b1-lab:~$ ^C
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ grep "^Port" /etc/ssh/sshd_config
Port 20022
agent-admin@b1-lab:~$ grep "^PermitRootLogin" /etc/ssh/sshd_config
PermitRootLogin no
agent-admin@b1-lab:~$ sudo ss -tulnp | grep sshd
tcp   LISTEN 0      128                0.0.0.0:20022      0.0.0.0:*    users:(("sshd",pid=268,fd=3))            
tcp   LISTEN 0      128                   [::]:20022         [::]:*    users:(("sshd",pid=268,fd=4))            
agent-admin@b1-lab:~$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere                  
15034/tcp                  ALLOW       Anywhere                  
20022/tcp (v6)             ALLOW       Anywhere (v6)             
15034/tcp (v6)             ALLOW       Anywhere (v6)             

agent-admin@b1-lab:~$ id agent-admin && id agent-dev && id agent-test
uid=1000(agent-admin) gid=1002(agent-admin) groups=1002(agent-admin),27(sudo),1000(agent-common),1001(agent-core)
uid=1001(agent-dev) gid=1003(agent-dev) groups=1003(agent-dev),1000(agent-common),1001(agent-core)
uid=1002(agent-test) gid=1004(agent-test) groups=1004(agent-test),1000(agent-common)
agent-admin@b1-lab:~$ sudo ls -la /home/agent-admin/agent-app/
total 13712
drwxr-x---  1 agent-admin agent-core      142 May 23 21:36 .
drwxr-x---  1 agent-admin agent-core      206 May 24 20:21 ..
-rwxr-x---  1 agent-dev   agent-core  7537848 May 18 17:06 agent-app-linux-arm64
-rwxr-xr-x  1 agent-admin agent-admin 6498144 May 20 11:11 agent-app-linux-x86
drwxrwx---+ 1 agent-admin agent-admin      44 May 23 21:28 api_keys
drwxr-xr-x  1 agent-admin agent-admin      20 May 24 19:04 bin
drwxr-xr-x  1 agent-admin agent-admin      88 May 23 21:36 __MACOSX
drwxrwsr-x+ 1 agent-admin agent-admin       0 May 23 19:52 upload_files
agent-admin@b1-lab:~$ sudo ls -la /var/log/agent-app
total 720
drwxrwx---+ 1 agent-admin agent-admin     80 May 24 20:23 .
drwxrwxr-x  1 root        syslog         278 May 23 21:34 ..
-rw-rw----+ 1 agent-admin agent-admin 724173 May 24 20:38 agent_app.log
-rw-rw----+ 1 agent-admin agent-admin   7536 May 24 20:38 monitor_cron.log
-rw-rw----+ 1 agent-admin agent-admin   1240 May 24 20:38 monitor.log
agent-admin@b1-lab:~$ getfacl /var/log/agent-app
getfacl: Removing leading '/' from absolute path names
# file: var/log/agent-app
# owner: agent-admin
# group: agent-admin
user::rwx
group::rwx
group:agent-core:rwx
mask::rwx
other::---
default:user::rwx
default:group::rwx
default:group:agent-core:rwx
default:mask::rwx
default:other::---

agent-admin@b1-lab:~$ cat /home/agent-admin/agent-app/api_keys/t_secret.key
agent_api_key_test
agent-admin@b1-lab:~$ pgrep -f agent-app-linux-x86
ss -tulnp | grep 15034
1312
1313
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*    users:(("agent-app-linux",pid=1313,fd=4))
agent-admin@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
-rwxr-x--- 1 agent-admin agent-core 5104 May 24 19:04 /home/agent-admin/agent-app/bin/monitor.sh
agent-admin@b1-lab:~$ crontab -l | grep monitor
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
agent-admin@b1-lab:~$ tail -20 /var/log/agent-app/monitor.log
[2026-05-24 19:05:55] PID:1312 CPU:0.0% MEM:3.7% DISK_USED:1%
[2026-05-24 19:08:41] PID:1312 CPU:0.0% MEM:4.5% DISK_USED:1%
[2026-05-24 19:11:06] PID:1312 CPU:0.0% MEM:4.0% DISK_USED:1%
[2026-05-24 19:16:31] PID:1312 CPU:0.0% MEM:3.4% DISK_USED:1%
[2026-05-24 20:23:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:24:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:25:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:26:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:27:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:28:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:29:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:30:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:31:01] PID:1312 CPU:0.0% MEM:5.0% DISK_USED:1%
[2026-05-24 20:32:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:33:01] PID:1312 CPU:1.1% MEM:4.8% DISK_USED:1%
[2026-05-24 20:34:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:35:01] PID:1312 CPU:1.1% MEM:4.8% DISK_USED:1%
[2026-05-24 20:36:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:37:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:38:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
agent-admin@b1-lab:~$ ^C
agent-admin@b1-lab:~$ echo "=== 1. SSH PORT ===" && grep "^Port" /etc/ssh/sshd_config && \
echo "=== 2. ROOT LOGIN ===" && grep "^PermitRootLogin" /etc/ssh/sshd_config && \
echo "=== 3. UFW ===" && sudo ufw status && \
echo "=== 4. ACCOUNTS ===" && id agent-admin && id agent-dev && id agent-test && \
echo "=== 5. CRONTAB ===" && crontab -l | grep monitor && \
echo "=== 6. LOG ===" && tail -5 /var/log/agent-app/monitor.log
=== 1. SSH PORT ===
Port 20022
=== 2. ROOT LOGIN ===
PermitRootLogin no
=== 3. UFW ===
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere                  
15034/tcp                  ALLOW       Anywhere                  
20022/tcp (v6)             ALLOW       Anywhere (v6)             
15034/tcp (v6)             ALLOW       Anywhere (v6)             

=== 4. ACCOUNTS ===
uid=1000(agent-admin) gid=1002(agent-admin) groups=1002(agent-admin),27(sudo),1000(agent-common),1001(agent-core)
uid=1001(agent-dev) gid=1003(agent-dev) groups=1003(agent-dev),1000(agent-common),1001(agent-core)
uid=1002(agent-test) gid=1004(agent-test) groups=1004(agent-test),1000(agent-common)
=== 5. CRONTAB ===
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
=== 6. LOG ===
[2026-05-24 20:35:01] PID:1312 CPU:1.1% MEM:4.8% DISK_USED:1%
[2026-05-24 20:36:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:37:01] PID:1312 CPU:0.0% MEM:4.9% DISK_USED:1%
[2026-05-24 20:38:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
[2026-05-24 20:39:01] PID:1312 CPU:0.0% MEM:4.8% DISK_USED:1%
agent-admin@b1-lab:~$ 
