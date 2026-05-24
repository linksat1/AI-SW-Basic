Last login: Sat May 23 21:40:04 on ttys011
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ sudo kill $(sudo lsof -t -i:15034)
sudo: lsof: command not found

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
cspag5955@b1-lab:~$ ./agent-app-linux-x86
-bash: ./agent-app-linux-x86: No such file or directory
cspag5955@b1-lab:~$ sudo fuser -k 15034/tcp
sudo: fuser: command not found
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
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export AGENT_LOG_DIR=/var/log/agent-app
agent-admin@b1-lab:~/agent-app$ ./agent-app-linux-x86
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
agent-admin@b1-lab:~/agent-app$ exit
logout
-bash: cd: /home/agent-admin/agent-app: Permission denied
-bash: ./agent-app-linux-x86: No such file or directory
cspag5955@b1-lab:~$ √
-bash: √: command not found
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
  [Restored May 24, 2026 at 2:49:14 PM]
Last login: Sun May 24 14:49:14 on ttys008
Restored session: Sat May 23 23:02:21 KST 2026
cspag5955@c5r5s1 ~ % 






















