Last login: Sun May 24 14:49:15 on ttys009
cspag5955@c5r5s1 ~ % ss -tulnp | grep 15034
zsh: command not found: ss
cspag5955@c5r5s1 ~ % netstat -tulnp | grep 15034
netstat: option requires an argument -- p
Usage:	netstat [-AaLlnW] [-f address_family | -p protocol]
	netstat [-gilns] [-f address_family]
	netstat -i | -I interface [-w wait] [-abdgRtS]
	netstat -s [-s] [-f address_family | -p protocol] [-w wait]
	netstat -i | -I interface -s [-f address_family | -p protocol]
	netstat -m [-m]
	netstat -r [-Aaln] [-f address_family]
	netstat -rs [-s]

cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ ss -tulnp | grep 15034
tcp   LISTEN 0      1                  0.0.0.0:15034      0.0.0.0:*          
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ exit
logout
Connection to 127.0.0.1 closed.
cspag5955@c5r5s1 ~ % ssh b1-lab@orb
cspag5955@b1-lab:~$ sudo groupadd agent-core
groupadd: group 'agent-core' already exists
cspag5955@b1-lab:~$ sudo useradd -m agent-dev
useradd: user 'agent-dev' already exists
cspag5955@b1-lab:~$ sudo usermod -aG agent-core agent-admin
cspag5955@b1-lab:~$ sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ ls -l /home/agent-admin/agent-app/bin/monitor.sh
ls: cannot access '/home/agent-admin/agent-app/bin/monitor.sh': Permission denied
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
-rwxr-x--- 1 agent-dev agent-core 5260 May 24 15:55 /home/agent-admin/agent-app/bin/monitor.sh
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ 
cspag5955@b1-lab:~$ su - agent-admin
Password: 
agent-admin@b1-lab:~$ /home/agent-admin/agent-app/bin/monitor.sh
/home/agent-admin/agent-app/bin/monitor.sh: line 1: cspag5955@c5r5s1: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 2: cspag5955@b1-lab:~$: command not found
/home/agent-admin/agent-app/bin/monitor.sh: line 3: tcp: command not found

====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent_app.py'... [FAIL] Process not running!
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ 
agent-admin@b1-lab:~$ sudo head -5 /home/agent-admin/agent-app/bin/monitor.sh
[sudo] password for agent-admin: 
agent-admin is not in the sudoers file.  This incident will be reported.
agent-admin@b1-lab:~$ exit
logout
cspag5955@b1-lab:~$ exit
logout
Connection to 127.0.0.1 closed.
cspag5955@c5r5s1 ~ % exit
sudo head -5 /home/agent-admin/agent-app/bin/monitor.sh

Saving session...
...copying shared history...
...saving history...truncating history files...
...completed.

[Process completed]





















