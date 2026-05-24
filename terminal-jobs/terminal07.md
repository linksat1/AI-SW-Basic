Last login: Sat May 23 21:19:15 on ttys009
cspag5955@c5r5s1 ~ % orb restart b1-lab
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ls /tmp/
cspag5955@b1-lab:~$ cp ~/Downloads/agent-app.zip /tmp/
orb push b1-lab /tmp/agent-app.zip /tmp/agent-app.zip
cp: cannot stat '/home/cspag5955/Downloads/agent-app.zip': No such file or directory

    ╭───────────────────────────────────────────────────────╮
    │                                                       │
    │              OrbStack update available!               │
    │              Run "orb update" to update.              │
    │                                                       │
    │  Updates include improvements, features, and fixes.   │
    │                                                       │
    ╰───────────────────────────────────────────────────────╯

cp: target '/tmp/agent-app.zip': No such file or directory
cspag5955@b1-lab:~$ cp /mnt/mac/Users/cspag5955/Downloads/agent-app.zip /tmp/agent-app.zip
ls -la /tmp/agent-app.zip
-rw-r--r-- 1 cspag5955 cspag5955 13847175 May 23 21:35 /tmp/agent-app.zip
cspag5955@b1-lab:~$ sudo mkdir -p /home/agent-admin/agent-app/api_keys
sudo mkdir -p /home/agent-admin/agent-app/upload_files
sudo mkdir -p /home/agent-admin/agent-app/bin
cspag5955@b1-lab:~$ sudo mkdir -p /home/agent-admin/agent-app/api_keys
cspag5955@b1-lab:~$ sudo mkdir -p /home/agent-admin/agent-app/upload_files
cspag5955@b1-lab:~$ sudo mkdir -p /home/agent-admin/agent-app/bin
cspag5955@b1-lab:~$ sudo unzip /tmp/agent-app.zip -d /home/agent-admin/agent-app/
Archive:  /tmp/agent-app.zip
replace /home/agent-admin/agent-app/agent-app-linux-x86? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: /home/agent-admin/agent-app/agent-app-linux-x86  
replace /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-x86? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-x86  
replace /home/agent-admin/agent-app/agent-app-linux-arm64? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: /home/agent-admin/agent-app/agent-app-linux-arm64  
replace /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-arm64? [y]es, [n]o, [A]ll, [N]one, [r]ename: y
  inflating: /home/agent-admin/agent-app/__MACOSX/._agent-app-linux-arm64  
cspag5955@b1-lab:~$ sudo chown -R agent-admin:agent-admin /home/agent-admin/agent-app/
cspag5955@b1-lab:~$ sudo ls -la /home/agent-admin/agent-app/
total 13712
drwxr-xr-x  1 agent-admin agent-admin     142 May 23 21:36 .
drwxr-x---  1 agent-admin agent-admin      98 May 23 20:39 ..
drwxr-xr-x  1 agent-admin agent-admin      88 May 23 21:36 __MACOSX
-rw-r--r--  1 agent-admin agent-admin 7537848 May 18 17:06 agent-app-linux-arm64
-rwxr-xr-x  1 agent-admin agent-admin 6498144 May 20 11:11 agent-app-linux-x86
drwxrwx---+ 1 agent-admin agent-admin      44 May 23 21:28 api_keys
drwxr-xr-x  1 agent-admin agent-admin       0 May 23 19:52 bin
drwxrwsr-x+ 1 agent-admin agent-admin       0 May 23 19:52 upload_files
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/t_secret.key
agent-admin@b1-lab:~$ cat /home/agent-admin/agent-app/api_keys/t_secret.key
agent_api_key_test
agent-admin@b1-lab:~$ chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key
agent-admin@b1-lab:~$ ls -la /home/agent-admin/agent-app/api_keys/
total 8
drwxrwx---+ 1 agent-admin agent-admin  44 May 23 21:28 .
drwxr-xr-x  1 agent-admin agent-admin 142 May 23 21:36 ..
-rw-------+ 1 agent-admin agent-admin  19 May 23 20:41 secret.key
-rw-------+ 1 agent-admin agent-admin  19 May 23 21:37 t_secret.key
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ export AGENT_HOME=/home/agent-admin/agent-app
agent-admin@b1-lab:~$ export AGENT_PORT=15034
agent-admin@b1-lab:~$ export AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
agent-admin@b1-lab:~$ export AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
agent-admin@b1-lab:~$ cd /home/agent-admin/agent-app
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
2026-05-23 21:39:22,580 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-05-23 21:39:22,580 [INFO] Agent listening at port 15034
2026-05-23 21:39:22,580 [INFO] === Agent Worker Started ===
2026-05-23 21:39:22,580 [INFO]    > Cycle: 0 -> 256MB/Lv10 -> 0
2026-05-23 21:39:22,580 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:39:22,617 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:39:22,618 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:39:24,624 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:39:24,663 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:39:24,663 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:39:27,671 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:39:27,710 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:39:27,710 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:39:31,717 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:39:31,755 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:39:31,755 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:39:36,763 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:39:36,800 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:39:36,800 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:39:42,806 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:39:42,844 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:39:42,844 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:39:48,910 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:39:48,967 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:39:48,967 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:39:54,973 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:39:55,011 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:39:55,011 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:40:01,019 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:40:01,057 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:40:01,058 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:40:07,065 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:40:07,104 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:40:07,105 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:40:13,111 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:40:13,150 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:40:13,150 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:40:19,156 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:40:19,156 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:40:19,158 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:40:19,158 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:40:25,165 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:40:25,167 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:40:25,167 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:40:31,173 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:40:31,174 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:40:31,175 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:40:37,181 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:40:37,182 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:40:37,183 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:40:43,190 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:40:43,191 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:40:43,191 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:40:49,200 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:40:49,202 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:40:49,202 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:40:54,210 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:40:54,211 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:40:54,211 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:40:58,218 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:40:58,219 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:40:58,219 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:41:01,225 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:41:01,226 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:41:01,227 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:41:03,234 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:41:03,235 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:41:04,241 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:41:04,242 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:41:05,248 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:41:05,248 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:41:05,252 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:41:05,253 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:41:07,260 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:41:07,268 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:41:07,268 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:41:10,275 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:41:10,313 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:41:10,313 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:41:14,319 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:41:14,357 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:41:14,357 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:41:19,360 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:41:19,399 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:41:19,399 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:41:25,406 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:41:25,437 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:41:25,437 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:41:31,444 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:41:31,483 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:41:31,484 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:41:37,493 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:41:37,529 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:41:37,529 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:41:43,536 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:41:43,575 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:41:43,575 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:41:49,583 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:41:49,622 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:41:49,622 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:41:55,630 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:41:55,666 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:41:55,666 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:42:01,674 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:42:01,675 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:42:01,675 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:42:01,675 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:42:07,682 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:42:07,683 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:42:07,684 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:42:13,691 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:42:13,691 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:42:13,691 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:42:19,698 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:42:19,700 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:42:19,700 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:42:25,707 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:42:25,708 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:42:25,708 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:42:31,716 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:42:31,718 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:42:31,718 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:42:36,725 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:42:36,726 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:42:36,726 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:42:40,734 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:42:40,740 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:42:40,740 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:42:43,746 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:42:43,746 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:42:43,746 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:42:45,753 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:42:45,755 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:42:46,761 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:42:46,762 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:42:47,768 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:42:47,769 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:42:47,771 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:42:47,771 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:42:49,779 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:42:49,818 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:42:49,818 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:42:52,826 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:42:52,864 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:42:52,864 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:42:56,871 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:42:56,909 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:42:56,909 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:43:01,916 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:43:01,954 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:43:01,954 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:43:07,961 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:43:08,000 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:43:08,000 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:43:14,007 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:43:14,045 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:43:14,045 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:43:20,052 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:43:20,090 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:43:20,090 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:43:26,097 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:43:26,126 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:43:26,126 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:43:32,132 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:43:32,170 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:43:32,170 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:43:38,177 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:43:38,214 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:43:38,214 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:43:44,221 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:43:44,222 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:43:44,222 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:43:44,222 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:43:50,229 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:43:50,231 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:43:50,231 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:43:56,238 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:43:56,239 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:43:56,239 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:44:02,246 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:44:02,248 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:44:02,248 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:44:08,255 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:44:08,256 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:44:08,256 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:44:14,263 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:44:14,265 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:44:14,265 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:44:19,272 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:44:19,273 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:44:19,273 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:44:23,281 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:44:23,282 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:44:23,283 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:44:26,289 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:44:26,289 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:44:26,290 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:44:28,297 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:44:28,299 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:44:29,305 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:44:29,305 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:44:30,312 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:44:30,312 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:44:30,314 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:44:30,314 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:44:32,321 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:44:32,359 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:44:32,360 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:44:35,366 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:44:35,515 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:44:35,515 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:44:39,560 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:44:39,597 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:44:39,597 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:44:44,605 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:44:44,643 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:44:44,643 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:44:50,649 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:44:50,687 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:44:50,688 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:44:56,694 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:44:56,733 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:44:56,733 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:45:02,740 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:45:02,778 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:45:02,778 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:45:08,785 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:45:08,823 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:45:08,823 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:45:14,831 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:45:14,869 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:45:14,870 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:45:20,877 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:45:20,916 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:45:20,916 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:45:26,922 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:45:26,922 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:45:26,923 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:45:26,923 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:45:32,930 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:45:32,933 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:45:32,933 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:45:38,941 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:45:38,941 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:45:38,942 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:45:44,949 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:45:44,950 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:45:44,950 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:45:50,956 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:45:50,956 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:45:50,956 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:45:56,963 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:45:56,965 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:45:56,966 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:46:01,972 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:46:01,973 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:46:01,973 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:46:05,980 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:46:05,983 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:46:05,983 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:46:08,991 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:46:08,991 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:46:08,991 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:46:11,048 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:46:11,049 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:46:12,056 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:46:12,056 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:46:13,064 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:46:13,064 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:46:13,066 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:46:13,066 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:46:15,074 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:46:15,112 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:46:15,112 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:46:18,120 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:46:18,159 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:46:18,159 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:46:22,166 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:46:22,209 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:46:22,210 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:46:27,217 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:46:27,255 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:46:27,256 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:46:33,263 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:46:33,301 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:46:33,302 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:46:39,310 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:46:39,348 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:46:39,349 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:46:45,355 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:46:45,393 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:46:45,393 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:46:51,402 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:46:51,441 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:46:51,441 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:46:57,448 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:46:57,486 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:46:57,486 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:47:03,494 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:47:03,532 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:47:03,532 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:47:09,540 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:47:09,540 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:47:09,541 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:47:09,541 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:47:15,547 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:47:15,549 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:47:15,549 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:47:21,556 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:47:21,556 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:47:21,556 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:47:27,563 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:47:27,565 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:47:27,565 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:47:33,572 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:47:33,572 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:47:33,573 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:47:39,579 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:47:39,581 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:47:39,581 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:47:44,587 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:47:44,588 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:47:44,588 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:47:48,595 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:47:48,597 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:47:48,598 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:47:51,605 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:47:51,605 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:47:51,605 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:47:53,612 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:47:53,614 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:47:54,621 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:47:54,621 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:47:55,628 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:47:55,628 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:47:55,630 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:47:55,630 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:47:57,632 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:47:57,670 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:47:57,670 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:48:00,677 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:48:00,715 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:48:00,716 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:48:04,724 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:48:04,763 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:48:04,763 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:48:09,770 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:48:09,808 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:48:09,808 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:48:15,814 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:48:15,853 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:48:15,853 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:48:21,860 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:48:21,898 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:48:21,898 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:48:27,905 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:48:27,943 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:48:27,943 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:48:33,950 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:48:33,982 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:48:33,982 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:48:39,989 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:48:40,014 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:48:40,014 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:48:46,021 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:48:46,060 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:48:46,061 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:48:52,069 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:48:52,069 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:48:52,070 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:48:52,070 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:48:58,077 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:48:58,080 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:48:58,080 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:49:04,086 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:49:04,086 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:49:04,087 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:49:10,095 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:49:10,097 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:49:10,098 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:49:16,106 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:49:16,106 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:49:16,106 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:49:22,113 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:49:22,115 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:49:22,115 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:49:27,123 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:49:27,123 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:49:27,124 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:49:31,132 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:49:31,134 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:49:31,134 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:49:34,140 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:49:34,140 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:49:34,140 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:49:36,149 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:49:36,151 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:49:37,158 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:49:37,158 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:49:38,165 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:49:38,165 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:49:38,167 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:49:38,167 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:49:40,174 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:49:40,212 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:49:40,213 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:49:43,220 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:49:43,260 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:49:43,260 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:49:47,268 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:49:47,307 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:49:47,307 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:49:52,313 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:49:52,352 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:49:52,352 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:49:58,358 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:49:58,395 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:49:58,396 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:50:04,402 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:50:04,440 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:50:04,440 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:50:10,448 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:50:10,483 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:50:10,483 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:50:16,490 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:50:16,528 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:50:16,529 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:50:22,537 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:50:22,575 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:50:22,575 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:50:28,582 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:50:28,620 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:50:28,620 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:50:34,628 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:50:34,628 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:50:34,629 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:50:34,629 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:50:40,636 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:50:40,638 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:50:40,638 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:50:46,644 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:50:46,645 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:50:46,645 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:50:52,653 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:50:52,655 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:50:52,655 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:50:58,662 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:50:58,662 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:50:58,663 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:51:04,669 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:51:04,671 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:51:04,671 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:51:09,679 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:51:09,679 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:51:09,679 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:51:13,687 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:51:13,689 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:51:13,689 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:51:16,696 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:51:16,696 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:51:16,697 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:51:18,702 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:51:18,704 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:51:19,711 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:51:19,711 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:51:20,717 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:51:20,718 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:51:20,720 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:51:20,720 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:51:22,728 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:51:22,766 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:51:22,766 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:51:25,773 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:51:25,811 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:51:25,811 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:51:29,819 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:51:29,858 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:51:29,858 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:51:34,865 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:51:34,901 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:51:34,901 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:51:40,908 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:51:40,943 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:51:40,943 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:51:47,026 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:51:47,093 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:51:47,093 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:51:53,099 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:51:53,136 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:51:53,136 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:51:59,143 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:51:59,181 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:51:59,182 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:52:05,189 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:52:05,219 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:52:05,219 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:52:11,226 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:52:11,264 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:52:11,264 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:52:17,270 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:52:17,270 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:52:17,270 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:52:17,270 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:52:23,277 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:52:23,279 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:52:23,280 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:52:29,286 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:52:29,286 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:52:29,286 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:52:35,294 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:52:35,296 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:52:35,296 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:52:41,304 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:52:41,305 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:52:41,305 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:52:47,312 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:52:47,314 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:52:47,314 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:52:52,320 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:52:52,320 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:52:52,320 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:52:56,326 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:52:56,327 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:52:56,327 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:52:59,335 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:52:59,335 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:52:59,335 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:53:01,343 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:53:01,345 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:53:02,350 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:53:02,351 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:53:03,357 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:53:03,358 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:53:03,360 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:53:03,360 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:53:05,368 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:53:05,406 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:53:05,406 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:53:08,414 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:53:08,449 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:53:08,449 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:53:12,457 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:53:12,495 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:53:12,496 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:53:17,503 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:53:17,540 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:53:17,540 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:53:23,548 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:53:23,586 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:53:23,587 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:53:29,593 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:53:29,631 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:53:29,631 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:53:35,639 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:53:35,677 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:53:35,677 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:53:41,684 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:53:41,723 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:53:41,723 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:53:47,729 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:53:47,767 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:53:47,768 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:53:53,778 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:53:53,816 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:53:53,816 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:53:59,823 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:53:59,823 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:53:59,823 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:53:59,824 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:54:05,831 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:54:05,833 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:54:05,834 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:54:11,841 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:54:11,842 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:54:11,842 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:54:17,849 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:54:17,850 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:54:17,851 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:54:23,857 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:54:23,857 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:54:23,858 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:54:29,864 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:54:29,866 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:54:29,866 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:54:34,874 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:54:34,874 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:54:34,874 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:54:38,880 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:54:38,882 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:54:38,883 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:54:41,888 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:54:41,888 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:54:41,889 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:54:43,896 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:54:43,898 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:54:44,904 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:54:44,904 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:54:45,911 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:54:45,911 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:54:45,913 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:54:45,914 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:54:47,920 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:54:47,930 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:54:47,930 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:54:50,937 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:54:50,941 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:54:50,941 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:54:54,948 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:54:54,987 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:54:54,987 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:54:59,994 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:55:00,032 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:55:00,032 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:55:06,039 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:55:06,077 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:55:06,077 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:55:12,085 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:55:12,123 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:55:12,123 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:55:18,132 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:55:18,170 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:55:18,170 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:55:24,173 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:55:24,210 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:55:24,210 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:55:30,217 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:55:30,255 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:55:30,255 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:55:36,263 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:55:36,303 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:55:36,303 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:55:42,310 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:55:42,310 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:55:42,310 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:55:42,311 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:55:48,318 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:55:48,320 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:55:48,320 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:55:54,328 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:55:54,328 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:55:54,329 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:56:00,336 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:56:00,338 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:56:00,339 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:56:06,345 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:56:06,345 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:56:06,345 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:56:12,352 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:56:12,355 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:56:12,355 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:56:17,362 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:56:17,362 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:56:17,362 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:56:21,369 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:56:21,371 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:56:21,371 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:56:24,379 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:56:24,379 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:56:24,379 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:56:26,386 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:56:26,388 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:56:27,395 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:56:27,395 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:56:28,401 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:56:28,401 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:56:28,403 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:56:28,403 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:56:30,411 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:56:30,452 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:56:30,452 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:56:33,459 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:56:33,497 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:56:33,497 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:56:37,504 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:56:37,541 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:56:37,541 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:56:42,547 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:56:42,588 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:56:42,588 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:56:48,595 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:56:48,633 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:56:48,634 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:56:54,641 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:56:54,669 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:56:54,670 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:57:00,677 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:57:00,715 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:57:00,716 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:57:06,722 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:57:06,761 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:57:06,761 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:57:12,767 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:57:12,805 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:57:12,805 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:57:18,881 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:57:18,932 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:57:18,932 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:57:24,940 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:57:24,941 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:57:24,941 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:57:24,941 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:57:30,949 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:57:30,951 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:57:30,951 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:57:36,958 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:57:36,958 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:57:36,958 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:57:42,965 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:57:42,967 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:57:42,968 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:57:48,997 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:57:48,997 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:57:48,997 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:57:55,004 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:57:55,006 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:57:55,007 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:58:00,013 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:58:00,014 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:58:00,014 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:58:04,021 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:58:04,023 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:58:04,023 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:58:07,030 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:58:07,031 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:58:07,031 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:58:09,036 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:58:09,038 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:58:10,045 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:58:10,045 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:58:11,052 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:58:11,052 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:58:11,054 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:58:11,055 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:58:13,062 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:58:13,100 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:58:13,100 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:58:16,107 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:58:16,145 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:58:16,146 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:58:20,152 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 21:58:20,191 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 21:58:20,192 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:58:25,199 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 21:58:25,236 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 21:58:25,237 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:58:31,244 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 21:58:31,282 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 21:58:31,282 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:58:37,289 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 21:58:37,334 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 21:58:37,334 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:58:43,341 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 21:58:43,380 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 21:58:43,380 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:58:49,387 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 21:58:49,425 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 21:58:49,425 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:58:55,431 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 21:58:55,470 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 21:58:55,470 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:59:01,477 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 21:59:01,515 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 21:59:01,515 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 21:59:07,522 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 21:59:07,523 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 21:59:07,523 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 21:59:07,523 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 21:59:13,529 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 21:59:13,531 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 21:59:13,531 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 21:59:19,537 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 21:59:19,538 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 21:59:19,538 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 21:59:25,546 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 21:59:25,548 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 21:59:25,548 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 21:59:31,555 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 21:59:31,556 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 21:59:31,556 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 21:59:37,564 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 21:59:37,566 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 21:59:37,566 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 21:59:42,573 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 21:59:42,574 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 21:59:42,574 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 21:59:46,581 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 21:59:46,584 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 21:59:46,584 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:59:49,591 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 21:59:49,592 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 21:59:49,592 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:59:51,600 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 21:59:51,602 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 21:59:52,607 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 21:59:52,608 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 21:59:53,614 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 21:59:53,614 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 21:59:53,616 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 21:59:53,616 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 21:59:55,623 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 21:59:55,663 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 21:59:55,663 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 21:59:58,671 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 21:59:58,710 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 21:59:58,710 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:00:02,717 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:00:02,756 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:00:02,756 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:00:07,763 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:00:07,802 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:00:07,802 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:00:13,809 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:00:13,847 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:00:13,847 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:00:19,855 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:00:19,893 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:00:19,893 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:00:25,900 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:00:25,944 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:00:25,945 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:00:31,953 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:00:31,992 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:00:31,992 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:00:37,999 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:00:38,038 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:00:38,039 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:00:44,045 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:00:44,086 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:00:44,086 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:00:50,093 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:00:50,094 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:00:50,094 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:00:50,094 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:00:56,101 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:00:56,103 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:00:56,103 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:01:02,111 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:01:02,111 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:01:02,111 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:01:08,119 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:01:08,120 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:01:08,121 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:01:14,127 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:01:14,127 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:01:14,128 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:01:20,136 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:01:20,138 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:01:20,138 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:01:25,146 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:01:25,147 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:01:25,147 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:01:29,154 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:01:29,155 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:01:29,156 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:01:32,163 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:01:32,164 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:01:32,164 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:01:34,172 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:01:34,174 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:01:35,180 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:01:35,181 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:01:36,187 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:01:36,187 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:01:36,189 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:01:36,189 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:01:38,196 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:01:38,234 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:01:38,234 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:01:41,241 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:01:41,280 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:01:41,280 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:01:45,288 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:01:45,328 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:01:45,328 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:01:50,336 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:01:50,374 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:01:50,374 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:01:56,380 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:01:56,430 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:01:56,430 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:02:02,438 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:02:02,478 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:02:02,478 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:02:08,487 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:02:08,525 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:02:08,525 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:02:14,532 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:02:14,574 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:02:14,574 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:02:20,581 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:02:20,621 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:02:20,622 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:02:26,627 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:02:26,665 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:02:26,665 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:02:32,671 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:02:32,671 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:02:32,671 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:02:32,671 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:02:38,681 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:02:38,683 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:02:38,683 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:02:44,690 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:02:44,691 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:02:44,691 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:02:50,698 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:02:50,700 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:02:50,700 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:02:56,709 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:02:56,710 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:02:56,710 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:03:02,719 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:03:02,721 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:03:02,721 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:03:07,729 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:03:07,729 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:03:07,729 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:03:11,737 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:03:11,739 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:03:11,739 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:03:14,745 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:03:14,746 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:03:14,746 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:03:16,752 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:03:16,754 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:03:17,761 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:03:17,762 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:03:18,768 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:03:18,769 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:03:18,771 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:03:18,771 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:03:20,783 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:03:20,821 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:03:20,821 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:03:23,829 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:03:23,867 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:03:23,867 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:03:27,876 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:03:27,914 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:03:27,914 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:03:32,924 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:03:32,962 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:03:32,962 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:03:38,971 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:03:39,008 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:03:39,009 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:03:45,018 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:03:45,055 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:03:45,056 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:03:51,065 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:03:51,102 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:03:51,102 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:03:57,110 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:03:57,147 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:03:57,147 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:04:03,156 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:04:03,194 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:04:03,195 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:04:09,204 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:04:09,241 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:04:09,242 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:04:15,250 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:04:15,250 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:04:15,250 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:04:15,250 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:04:21,258 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:04:21,260 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:04:21,260 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:04:27,269 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:04:27,270 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:04:27,270 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:04:33,278 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:04:33,280 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:04:33,280 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:04:39,286 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:04:39,287 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:04:39,287 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:04:45,293 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:04:45,295 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:04:45,296 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:04:50,304 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:04:50,305 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:04:50,305 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:04:54,312 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:04:54,314 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:04:54,314 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:04:57,322 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:04:57,322 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:04:57,323 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:04:59,329 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:04:59,331 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:05:00,339 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:05:00,339 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:05:01,347 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:05:01,348 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:05:01,350 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:05:01,350 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:05:03,359 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:05:03,397 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:05:03,398 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:05:06,407 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:05:06,445 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:05:06,445 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:05:10,451 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:05:10,491 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:05:10,491 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:05:15,500 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:05:15,539 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:05:15,539 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:05:21,548 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:05:21,585 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:05:21,585 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:05:27,593 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:05:27,631 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:05:27,631 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:05:33,641 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:05:33,679 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:05:33,679 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:05:39,688 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:05:39,725 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:05:39,726 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:05:45,734 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:05:45,772 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:05:45,773 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:05:51,778 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:05:51,817 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:05:51,817 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:05:57,825 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:05:57,825 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:05:57,825 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:05:57,825 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:06:03,833 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:06:03,833 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:06:03,833 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:06:09,839 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:06:09,839 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:06:09,840 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:06:15,847 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:06:15,847 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:06:15,847 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:06:21,856 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:06:21,856 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:06:21,856 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:06:27,865 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:06:27,866 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:06:27,866 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:06:32,874 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:06:32,874 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:06:32,874 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:06:36,882 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:06:36,882 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:06:36,882 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:06:39,890 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:06:39,891 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:06:39,891 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:06:41,899 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:06:41,899 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:06:42,907 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:06:42,907 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:06:43,914 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:06:43,915 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:06:43,917 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:06:43,917 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:06:45,926 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:06:45,928 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:06:45,928 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:06:48,938 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:06:48,940 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:06:48,940 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:06:52,947 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:06:52,949 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:06:52,950 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:06:57,959 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:06:57,961 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:06:57,961 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:07:03,970 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:07:03,972 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:07:03,973 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:07:09,981 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:07:09,983 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:07:09,983 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:07:15,991 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:07:15,993 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:07:15,993 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:07:22,001 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:07:22,004 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:07:22,004 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:07:28,011 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:07:28,013 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:07:28,013 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:07:34,021 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:07:34,023 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:07:34,023 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:07:40,030 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:07:40,030 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:07:40,030 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:07:40,031 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:07:46,038 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:07:46,038 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:07:46,038 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:07:52,046 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:07:52,046 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:07:52,046 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:07:58,053 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:07:58,054 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:07:58,054 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:08:04,062 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:08:04,063 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:08:04,063 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:08:10,070 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:08:10,071 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:08:10,071 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:08:15,079 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:08:15,079 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:08:15,079 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:08:19,087 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:08:19,087 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:08:19,087 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:08:22,096 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:08:22,096 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:08:22,096 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:08:24,104 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:08:24,104 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:08:25,112 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:08:25,112 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:08:26,119 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:08:26,120 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:08:26,122 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:08:26,123 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:08:28,132 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:08:28,134 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:08:28,135 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:08:31,142 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:08:31,144 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:08:31,145 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:08:35,153 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:08:35,155 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:08:35,155 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:08:40,164 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:08:40,167 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:08:40,167 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:08:46,176 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:08:46,178 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:08:46,178 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:08:52,187 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:08:52,190 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:08:52,190 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:08:58,199 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:08:58,201 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:08:58,201 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:09:04,211 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:09:04,213 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:09:04,213 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:09:10,221 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:09:10,224 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:09:10,224 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:09:16,232 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:09:16,234 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:09:16,234 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:09:22,242 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:09:22,242 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:09:22,242 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:09:22,242 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:09:28,250 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:09:28,250 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:09:28,250 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:09:34,257 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:09:34,258 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:09:34,258 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:09:40,266 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:09:40,266 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:09:40,266 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:09:46,274 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:09:46,275 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:09:46,275 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:09:52,284 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:09:52,284 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:09:52,284 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:09:57,294 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:09:57,295 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:09:57,295 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:10:01,301 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:10:01,302 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:10:01,302 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:10:04,311 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:10:04,312 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:10:04,312 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:10:06,321 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:10:06,322 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:10:07,329 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:10:07,330 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:10:08,336 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:10:08,336 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:10:08,338 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:10:08,338 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:10:10,346 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:10:10,348 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:10:10,349 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:10:13,356 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:10:13,358 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:10:13,359 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:10:17,367 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:10:17,369 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:10:17,369 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:10:22,378 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:10:22,380 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:10:22,381 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:10:28,387 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:10:28,390 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:10:28,390 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:10:34,399 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:10:34,401 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:10:34,401 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:10:40,409 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:10:40,411 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:10:40,411 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:10:46,421 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:10:46,424 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:10:46,424 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:10:52,432 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:10:52,434 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:10:52,434 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:10:58,441 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:10:58,443 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:10:58,443 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:11:04,452 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:11:04,453 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:11:04,453 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:11:04,453 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:11:10,462 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:11:10,462 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:11:10,462 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:11:16,470 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:11:16,470 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:11:16,471 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:11:22,478 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:11:22,478 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:11:22,479 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:11:28,485 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:11:28,485 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:11:28,486 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:11:34,494 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:11:34,494 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:11:34,494 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:11:39,502 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:11:39,502 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:11:39,503 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:11:43,510 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:11:43,511 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:11:43,511 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:11:46,520 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:11:46,520 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:11:46,520 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:11:48,528 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:11:48,529 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:11:49,536 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:11:49,537 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:11:50,544 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:11:50,544 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:11:50,547 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:11:50,547 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:11:52,556 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:11:52,558 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:11:52,558 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:11:55,566 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:11:55,568 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:11:55,569 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:11:59,576 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:11:59,578 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:11:59,578 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:12:04,586 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:12:04,588 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:12:04,588 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:12:10,595 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:12:10,597 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:12:10,598 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:12:16,605 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:12:16,607 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:12:16,607 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:12:22,617 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:12:22,619 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:12:22,619 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:12:28,627 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:12:28,629 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:12:28,629 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:12:34,638 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:12:34,640 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:12:34,640 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:12:40,649 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:12:40,651 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:12:40,651 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:12:46,660 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:12:46,660 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:12:46,660 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:12:46,660 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:12:52,668 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:12:52,669 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:12:52,669 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:12:58,677 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:12:58,677 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:12:58,677 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:13:04,685 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:13:04,685 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:13:04,686 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:13:10,693 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:13:10,694 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:13:10,694 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:13:16,702 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:13:16,703 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:13:16,703 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:13:21,710 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:13:21,711 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:13:21,711 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:13:25,718 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:13:25,719 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:13:25,719 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:13:28,726 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:13:28,727 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:13:28,727 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:13:30,735 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:13:30,735 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:13:31,744 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:13:31,744 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:13:32,752 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:13:32,753 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:13:32,755 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:13:32,755 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:13:34,764 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:13:34,766 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:13:34,766 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:13:37,775 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:13:37,777 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:13:37,777 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:13:41,786 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:13:41,789 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:13:41,789 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:13:46,796 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:13:46,798 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:13:46,799 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:13:52,805 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:13:52,808 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:13:52,808 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:13:58,816 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:13:58,818 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:13:58,818 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:14:04,827 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:14:04,829 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:14:04,829 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:14:10,836 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:14:10,839 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:14:10,839 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:14:16,847 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:14:16,849 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:14:16,849 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:14:22,857 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:14:22,859 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:14:22,859 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:14:28,869 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:14:28,869 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:14:28,869 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:14:28,869 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:14:34,877 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:14:34,878 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:14:34,878 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:14:40,887 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:14:40,887 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:14:40,888 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:14:46,896 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:14:46,897 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:14:46,897 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:14:52,904 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:14:52,905 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:14:52,905 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:14:58,913 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:14:58,913 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:14:58,913 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:15:03,923 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:15:03,923 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:15:03,923 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:15:07,932 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:15:07,933 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:15:07,933 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:15:10,942 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:15:10,942 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:15:10,942 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:15:12,950 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:15:12,950 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:15:13,958 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:15:13,958 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:15:14,965 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:15:14,966 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:15:14,968 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:15:14,968 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:15:16,976 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:15:16,979 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:15:16,979 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:15:19,988 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:15:19,990 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:15:19,990 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:15:23,996 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:15:23,998 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:15:23,998 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:15:29,006 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:15:29,008 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:15:29,008 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:15:35,017 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:15:35,019 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:15:35,019 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:15:41,025 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:15:41,027 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:15:41,028 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:15:47,034 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:15:47,036 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:15:47,036 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:15:53,045 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:15:53,048 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:15:53,048 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:15:59,056 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:15:59,058 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:15:59,058 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:16:05,067 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:16:05,069 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:16:05,070 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:16:11,078 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:16:11,079 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:16:11,079 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:16:11,079 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:16:17,088 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:16:17,088 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:16:17,088 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:16:23,097 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:16:23,097 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:16:23,097 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:16:29,104 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:16:29,105 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:16:29,105 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:16:35,112 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:16:35,113 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:16:35,113 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:16:41,122 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:16:41,122 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:16:41,123 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:16:46,131 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:16:46,132 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:16:46,132 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:16:50,140 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:16:50,141 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:16:50,141 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:16:53,150 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:16:53,151 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:16:53,151 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:16:55,160 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:16:55,160 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:16:56,167 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:16:56,167 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:16:57,174 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:16:57,175 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:16:57,177 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:16:57,177 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:16:59,185 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:16:59,188 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:16:59,188 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:17:02,197 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:17:02,200 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:17:02,200 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:17:06,208 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:17:06,210 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:17:06,211 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:17:11,218 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:17:11,220 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:17:11,220 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:17:17,229 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:17:17,231 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:17:17,231 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:17:23,237 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:17:23,239 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:17:23,240 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:17:29,246 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:17:29,248 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:17:29,248 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:17:35,256 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:17:35,258 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:17:35,258 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:17:41,266 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:17:41,269 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:17:41,269 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:17:47,276 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:17:47,278 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:17:47,279 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:17:53,287 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:17:53,288 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:17:53,288 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:17:53,288 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:17:59,296 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:17:59,296 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:17:59,296 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:18:05,305 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:18:05,305 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:18:05,305 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:18:11,314 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:18:11,314 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:18:11,314 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:18:17,324 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:18:17,324 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:18:17,324 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:18:23,334 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:18:23,334 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:18:23,334 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:18:28,343 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:18:28,344 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:18:28,344 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:18:32,353 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:18:32,353 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:18:32,353 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:18:35,362 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:18:35,362 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:18:35,363 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:18:37,372 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:18:37,372 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:18:38,380 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:18:38,380 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:18:39,387 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:18:39,388 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:18:39,390 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:18:39,390 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:18:41,399 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:18:41,402 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:18:41,402 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:18:44,411 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:18:44,414 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:18:44,414 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:18:48,423 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:18:48,425 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:18:48,425 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:18:53,433 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:18:53,435 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:18:53,435 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:18:59,444 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:18:59,446 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:18:59,446 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:19:05,454 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:19:05,457 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:19:05,457 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:19:11,466 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:19:11,468 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:19:11,468 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:19:17,477 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:19:17,480 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:19:17,480 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:19:23,489 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:19:23,491 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:19:23,491 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:19:29,499 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:19:29,502 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:19:29,502 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:19:35,511 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:19:35,511 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:19:35,512 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:19:35,512 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:19:41,520 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:19:41,521 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:19:41,521 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:19:47,528 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:19:47,529 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:19:47,529 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:19:53,536 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:19:53,536 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:19:53,537 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:19:59,544 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:19:59,545 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:19:59,545 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:20:05,552 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:20:05,552 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:20:05,553 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:20:10,560 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:20:10,560 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:20:10,560 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:20:14,569 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:20:14,569 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:20:14,569 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:20:17,577 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:20:17,577 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:20:17,577 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:20:19,585 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:20:19,585 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:20:20,593 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:20:20,593 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:20:21,601 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:20:21,601 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:20:21,603 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:20:21,603 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:20:23,612 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:20:23,614 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:20:23,614 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:20:26,624 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:20:26,626 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:20:26,626 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:20:30,635 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:20:30,637 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:20:30,637 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:20:35,646 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:20:35,648 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:20:35,648 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:20:41,656 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:20:41,658 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:20:41,659 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:20:47,666 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:20:47,669 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:20:47,669 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:20:53,677 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:20:53,679 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:20:53,679 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:20:59,686 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:20:59,688 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:20:59,689 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:21:05,696 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:21:05,699 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:21:05,699 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:21:11,706 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:21:11,709 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:21:11,709 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:21:17,718 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:21:17,718 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:21:17,719 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:21:17,719 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:21:23,726 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:21:23,726 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:21:23,726 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:21:29,734 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:21:29,734 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:21:29,734 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:21:35,743 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:21:35,744 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:21:35,744 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:21:41,750 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:21:41,750 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:21:41,750 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:21:47,759 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:21:47,760 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:21:47,760 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:21:52,767 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:21:52,767 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:21:52,767 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:21:56,776 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:21:56,776 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:21:56,776 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:21:59,784 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:21:59,784 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:21:59,785 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:22:01,792 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:22:01,792 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:22:02,800 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:22:02,801 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:22:03,808 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:22:03,809 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:22:03,811 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:22:03,811 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:22:05,818 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:22:05,821 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:22:05,821 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:22:08,829 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:22:08,831 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:22:08,831 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:22:12,840 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:22:12,842 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:22:12,842 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:22:17,851 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:22:17,854 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:22:17,854 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:22:23,861 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:22:23,864 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:22:23,864 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:22:29,872 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:22:29,874 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:22:29,874 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:22:35,881 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:22:35,883 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:22:35,884 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:22:41,893 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:22:41,895 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:22:41,896 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:22:47,905 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:22:47,907 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:22:47,907 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:22:53,916 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:22:53,918 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:22:53,919 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:22:59,926 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:22:59,927 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:22:59,927 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:22:59,927 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:23:05,936 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:23:05,937 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:23:05,937 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:23:11,945 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:23:11,945 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:23:11,945 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:23:17,952 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:23:17,953 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:23:17,953 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:23:23,960 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:23:23,961 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:23:23,961 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:23:29,970 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:23:29,971 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:23:29,971 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:23:34,977 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:23:34,978 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:23:34,978 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:23:38,988 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:23:38,988 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:23:38,988 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:23:41,996 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:23:41,997 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:23:41,997 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:23:44,006 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:23:44,006 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:23:45,014 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:23:45,014 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:23:46,022 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:23:46,022 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:23:46,024 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:23:46,024 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:23:48,034 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:23:48,036 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:23:48,036 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:23:51,045 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:23:51,048 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:23:51,048 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:23:55,055 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:23:55,057 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:23:55,058 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:24:00,068 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:24:00,070 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:24:00,070 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:24:06,080 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:24:06,082 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:24:06,082 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:24:12,091 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:24:12,094 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:24:12,094 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:24:18,102 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:24:18,104 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:24:18,104 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:24:24,113 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:24:24,115 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:24:24,115 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:24:30,124 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:24:30,127 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:24:30,127 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:24:36,136 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:24:36,139 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:24:36,139 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:24:42,145 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:24:42,145 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:24:42,145 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:24:42,146 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:24:48,155 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:24:48,156 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:24:48,156 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:24:54,164 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:24:54,164 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:24:54,164 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:25:00,172 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:25:00,172 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:25:00,172 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:25:06,181 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:25:06,181 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:25:06,181 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:25:12,189 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:25:12,189 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:25:12,189 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:25:17,198 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:25:17,198 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:25:17,198 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:25:21,206 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:25:21,206 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:25:21,206 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:25:24,215 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:25:24,216 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:25:24,216 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:25:26,225 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:25:26,226 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:25:27,233 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:25:27,234 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:25:28,240 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:25:28,240 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:25:28,242 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:25:28,242 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:25:30,251 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:25:30,253 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:25:30,254 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:25:33,260 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:25:33,263 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:25:33,263 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:25:37,272 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:25:37,274 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:25:37,275 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:25:42,283 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:25:42,286 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:25:42,286 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:25:48,294 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:25:48,296 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:25:48,296 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:25:54,304 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:25:54,306 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:25:54,306 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:26:00,313 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:26:00,316 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:26:00,316 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:26:06,325 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:26:06,327 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:26:06,327 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:26:12,336 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:26:12,338 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:26:12,338 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:26:18,347 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:26:18,350 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:26:18,350 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:26:24,358 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:26:24,358 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:26:24,358 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:26:24,358 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:26:30,366 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:26:30,366 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:26:30,366 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:26:36,374 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:26:36,374 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:26:36,374 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:26:42,383 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:26:42,383 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:26:42,383 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:26:48,391 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:26:48,392 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:26:48,392 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:26:54,401 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:26:54,401 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:26:54,401 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:26:59,410 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:26:59,411 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:26:59,411 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:27:03,419 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:27:03,420 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:27:03,420 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:27:06,428 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:27:06,428 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:27:06,428 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:27:08,435 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:27:08,435 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:27:09,443 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:27:09,443 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:27:10,451 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:27:10,451 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:27:10,454 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:27:10,454 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:27:12,462 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:27:12,464 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:27:12,464 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:27:15,472 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:27:15,474 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:27:15,474 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:27:19,483 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:27:19,486 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:27:19,486 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:27:24,495 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:27:24,497 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:27:24,497 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:27:30,505 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:27:30,507 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:27:30,507 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:27:36,516 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:27:36,518 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:27:36,518 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:27:42,528 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:27:42,530 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:27:42,530 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:27:48,540 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:27:48,542 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:27:48,542 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:27:54,551 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:27:54,553 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:27:54,553 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:28:00,562 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:28:00,564 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:28:00,564 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:28:06,573 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:28:06,573 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:28:06,573 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:28:06,573 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:28:12,582 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:28:12,583 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:28:12,583 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:28:18,590 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:28:18,590 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:28:18,590 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:28:24,599 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:28:24,599 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:28:24,599 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:28:30,607 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:28:30,607 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:28:30,607 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:28:36,616 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:28:36,616 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:28:36,616 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:28:41,625 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:28:41,626 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:28:41,626 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:28:45,635 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:28:45,635 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:28:45,635 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:28:48,642 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:28:48,642 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:28:48,642 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:28:50,650 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:28:50,651 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:28:51,658 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:28:51,658 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:28:52,666 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:28:52,666 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:28:52,668 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:28:52,669 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:28:54,678 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:28:54,680 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:28:54,680 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:28:57,689 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:28:57,691 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:28:57,691 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:29:01,699 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:29:01,701 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:29:01,701 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:29:06,709 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:29:06,711 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:29:06,711 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:29:12,720 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:29:12,722 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:29:12,722 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:29:18,728 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:29:18,730 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:29:18,730 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:29:24,739 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:29:24,742 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:29:24,742 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:29:30,750 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:29:30,752 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:29:30,753 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:29:36,761 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:29:36,764 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:29:36,764 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:29:42,771 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:29:42,773 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:29:42,774 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:29:48,782 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:29:48,782 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:29:48,782 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:29:48,782 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:29:54,792 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:29:54,792 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:29:54,792 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:30:00,800 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:30:00,800 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:30:00,800 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:30:06,808 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:30:06,809 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:30:06,809 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:30:12,818 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:30:12,818 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:30:12,818 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:30:18,828 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:30:18,828 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:30:18,828 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:30:23,838 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:30:23,838 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:30:23,838 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:30:27,846 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:30:27,846 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:30:27,846 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:30:30,852 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:30:30,853 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:30:30,853 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:30:32,862 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:30:32,862 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:30:33,869 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:30:33,870 [INFO] [Memory] Releasing... (-25MB) Total: 0MB
2026-05-23 22:30:34,876 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-05-23 22:30:34,876 [INFO] --- Step Info: Mode=UP, CPU Lv=1, Mem=0MB ---
2026-05-23 22:30:34,878 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-05-23 22:30:34,878 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:30:36,886 [INFO] --- Step Info: Mode=UP, CPU Lv=2, Mem=25MB ---
2026-05-23 22:30:36,889 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-05-23 22:30:36,889 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:30:39,898 [INFO] --- Step Info: Mode=UP, CPU Lv=3, Mem=50MB ---
2026-05-23 22:30:39,900 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-05-23 22:30:39,900 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:30:43,908 [INFO] --- Step Info: Mode=UP, CPU Lv=4, Mem=75MB ---
2026-05-23 22:30:43,910 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-05-23 22:30:43,910 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:30:48,919 [INFO] --- Step Info: Mode=UP, CPU Lv=5, Mem=100MB ---
2026-05-23 22:30:48,921 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-05-23 22:30:48,921 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:30:54,928 [INFO] --- Step Info: Mode=UP, CPU Lv=6, Mem=125MB ---
2026-05-23 22:30:54,931 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-05-23 22:30:54,931 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:31:00,940 [INFO] --- Step Info: Mode=UP, CPU Lv=7, Mem=150MB ---
2026-05-23 22:31:00,942 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-05-23 22:31:00,942 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:31:06,950 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=175MB ---
2026-05-23 22:31:06,952 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-05-23 22:31:06,952 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:31:12,960 [INFO] --- Step Info: Mode=UP, CPU Lv=9, Mem=200MB ---
2026-05-23 22:31:12,962 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-05-23 22:31:12,962 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:31:18,971 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-05-23 22:31:18,973 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-05-23 22:31:18,973 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:31:24,983 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-05-23 22:31:24,985 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB
2026-05-23 22:31:24,985 [INFO] [CPU] Occupy core for 5s (Level 10)
2026-05-23 22:31:30,992 [INFO] >>> PEAK REACHED (Max Load). Switching to RAMP DOWN. ▼ <<<
2026-05-23 22:31:30,992 [INFO] --- Step Info: Mode=DOWN, CPU Lv=9, Mem=275MB ---
2026-05-23 22:31:30,992 [INFO] [Memory] Releasing... (-25MB) Total: 250MB
2026-05-23 22:31:30,992 [INFO] [CPU] Occupy core for 5s (Level 9)
2026-05-23 22:31:37,001 [INFO] --- Step Info: Mode=DOWN, CPU Lv=8, Mem=250MB ---
2026-05-23 22:31:37,002 [INFO] [Memory] Releasing... (-25MB) Total: 225MB
2026-05-23 22:31:37,002 [INFO] [CPU] Occupy core for 5s (Level 8)
2026-05-23 22:31:43,011 [INFO] --- Step Info: Mode=DOWN, CPU Lv=7, Mem=225MB ---
2026-05-23 22:31:43,011 [INFO] [Memory] Releasing... (-25MB) Total: 200MB
2026-05-23 22:31:43,011 [INFO] [CPU] Occupy core for 5s (Level 7)
2026-05-23 22:31:49,020 [INFO] --- Step Info: Mode=DOWN, CPU Lv=6, Mem=200MB ---
2026-05-23 22:31:49,020 [INFO] [Memory] Releasing... (-25MB) Total: 175MB
2026-05-23 22:31:49,020 [INFO] [CPU] Occupy core for 5s (Level 6)
2026-05-23 22:31:55,029 [INFO] --- Step Info: Mode=DOWN, CPU Lv=5, Mem=175MB ---
2026-05-23 22:31:55,030 [INFO] [Memory] Releasing... (-25MB) Total: 150MB
2026-05-23 22:31:55,030 [INFO] [CPU] Occupy core for 5s (Level 5)
2026-05-23 22:32:01,038 [INFO] --- Step Info: Mode=DOWN, CPU Lv=4, Mem=150MB ---
2026-05-23 22:32:01,038 [INFO] [Memory] Releasing... (-25MB) Total: 125MB
2026-05-23 22:32:01,039 [INFO] [CPU] Occupy core for 4s (Level 4)
2026-05-23 22:32:06,046 [INFO] --- Step Info: Mode=DOWN, CPU Lv=3, Mem=125MB ---
2026-05-23 22:32:06,046 [INFO] [Memory] Releasing... (-25MB) Total: 100MB
2026-05-23 22:32:06,047 [INFO] [CPU] Occupy core for 3s (Level 3)
2026-05-23 22:32:10,055 [INFO] --- Step Info: Mode=DOWN, CPU Lv=2, Mem=100MB ---
2026-05-23 22:32:10,055 [INFO] [Memory] Releasing... (-25MB) Total: 75MB
2026-05-23 22:32:10,055 [INFO] [CPU] Occupy core for 2s (Level 2)
2026-05-23 22:32:13,063 [INFO] --- Step Info: Mode=DOWN, CPU Lv=1, Mem=75MB ---
2026-05-23 22:32:13,063 [INFO] [Memory] Releasing... (-25MB) Total: 50MB
2026-05-23 22:32:13,063 [INFO] [CPU] Occupy core for 1s (Level 1)
2026-05-23 22:32:15,073 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=50MB ---
2026-05-23 22:32:15,073 [INFO] [Memory] Releasing... (-25MB) Total: 25MB
2026-05-23 22:32:16,081 [INFO] --- Step Info: Mode=DOWN, CPU Lv=0, Mem=25MB ---
2026-05-23 22:32:16,082 [INFO] [Memory] Releasing... (-25MB) Total: 0MB

  [Restored May 24, 2026 at 2:49:14 PM]
Last login: Sun May 24 14:49:14 on ttys002
Restored session: Sat May 23 23:02:21 KST 2026
cspag5955@c5r5s1 ~ % 
