# B1-1 미션 단계별 실행 가이드
## 시스템 관제 자동화 스크립트 개발

> **대상:** 리눅스 입문자  
> **환경:** macOS + OrbStack / Ubuntu 22.04 LTS (x86_64)  
> **예상 소요 시간:** 약 2~3시간

---

## 📋 시작 전 체크리스트

| 항목 | 확인 |
|------|------|
| OrbStack 설치 및 b1-lab VM 생성 완료 | ☐ |
| `agent-app-linux-x86` 파일 존재 확인 | ☐ |
| 터미널 2개 준비 (앱 실행용 + 작업용) | ☐ |

---

## 🗺️ 전체 단계 흐름

```
[1단계] VM 접속 및 파일 준비
    ↓
[2단계] SSH 보안 설정 (포트 20022, root 차단)
    ↓
[3단계] 방화벽 설정 (UFW: 20022, 15034만 허용)
    ↓
[4단계] 계정/그룹 생성 (admin/dev/test, common/core)
    ↓
[5단계] 디렉토리 구조 및 권한 설정 (ACL 포함)
    ↓
[6단계] 앱 실행 환경 구성 (환경변수, 키 파일)
    ↓
[7단계] 앱 실행 확인 (Boot Sequence 5단계 [OK])
    ↓
[8단계] monitor.sh 작성
    ↓
[9단계] sudo NOPASSWD 설정
    ↓
[10단계] crontab 자동 실행 등록
    ↓
[11단계] 최종 검증 체크리스트
```

---

## 1단계: VM 접속 및 파일 준비

### 1-1. OrbStack VM에 접속

**macOS 터미널에서:**
```bash
# b1-lab VM에 접속
orb shell b1-lab
```

접속 성공 시 프롬프트가 바뀝니다:
```
ubuntu@b1-lab:~$   또는   (사용자명)@b1-lab:~$
```

### 1-2. OS 버전 및 기본 환경 확인

```bash
# Ubuntu 22.04 확인
lsb_release -a

# 현재 사용자 확인
whoami

# sudo 권한 확인
sudo whoami
```

**기대 출력:**
```
Description: Ubuntu 22.04.x LTS
whoami → ubuntu (또는 본인 계정명)
sudo whoami → root
```

### 1-3. 필수 패키지 설치

```bash
sudo apt update
sudo apt install -y acl ufw net-tools
```

### 1-4. 앱 파일을 VM으로 복사

**새 macOS 터미널을 열어서 (orb shell 밖에서 실행):**

```bash
# macOS에서 VM의 /tmp 로 파일 복사
orb push b1-lab /Users/cspag5955/cspag/AI-SW-Basic/agent-app/agent-app-linux-x86 /tmp/agent-app-linux-x86
```

**복사 확인 (VM 안에서):**
```bash
ls -la /tmp/agent-app-linux-x86
```

> 💡 **Tip:** OrbStack에서는 Mac 홈 디렉토리가 VM 내부에 `/mac/Users/사용자명/` 으로 자동 마운트됩니다.  
> 대안으로 VM 안에서 직접 접근: `ls /mac/Users/cspag5955/cspag/AI-SW-Basic/agent-app/`

---

## 2단계: SSH 보안 설정

### 왜 SSH 포트를 바꾸나요?
기본 22번 포트는 전 세계 해커의 자동화된 공격이 집중됩니다. 20022로 변경하면 자동화 공격 대부분을 회피합니다.
Root 원격 접속 차단은 비밀번호가 유출되어도 직접 서버를 장악하지 못하게 막습니다.

### 2-1. SSH 설정 파일 수정

```bash
sudo nano /etc/ssh/sshd_config
```

파일에서 아래 두 줄을 찾아서 수정합니다:

| 찾을 내용 | 변경할 내용 |
|----------|------------|
| `#Port 22` | `Port 20022` |
| `#PermitRootLogin prohibit-password` | `PermitRootLogin no` |

> **nano 편집기 단축키:**  
> `Ctrl+W` : 검색 → "Port" 검색하면 빠름  
> `Ctrl+O` → `Enter` : 저장  
> `Ctrl+X` : 종료  

### 2-2. SSH 서비스 재시작

```bash
sudo systemctl restart sshd
```

### 2-3. 설정 확인

```bash
# 설정 파일에서 확인
grep -E "^Port|^PermitRootLogin" /etc/ssh/sshd_config

# 실제 리슨 포트 확인
sudo ss -tulnp | grep sshd
```

**기대 출력:**
```
Port 20022
PermitRootLogin no
tcp  LISTEN  0  128  0.0.0.0:20022  0.0.0.0:*  users:(("sshd",...))
```

> ✅ **OrbStack 참고:** `orb shell` 접속은 SSH와 별개이므로, 포트 변경 후에도 `orb shell b1-lab`은 정상 동작합니다.

---

## 3단계: 방화벽 설정 (UFW)

### 왜 방화벽이 필요한가요?
서버의 "문지기" 역할입니다. SSH(20022)와 앱 포트(15034)만 열고 나머지는 모두 차단합니다.

> ⚠️ **중요:** `ufw enable` 전에 반드시 포트를 먼저 허용해야 합니다. 순서를 바꾸면 접속이 차단될 수 있습니다.

### 3-1. 포트 허용 후 UFW 활성화

```bash
# 1. SSH 포트 먼저 허용 (이 순서가 중요!)
sudo ufw allow 20022/tcp

# 2. 앱 포트 허용
sudo ufw allow 15034/tcp

# 3. UFW 활성화 (y 입력)
sudo ufw enable

# 4. 상태 확인
sudo ufw status
```

**기대 출력:**
```
Status: active

To                         Action      From
--                         ------      ----
20022/tcp                  ALLOW       Anywhere
15034/tcp                  ALLOW       Anywhere
20022/tcp (v6)             ALLOW       Anywhere (v6)
15034/tcp (v6)             ALLOW       Anywhere (v6)
```

---

## 4단계: 계정 및 그룹 생성

### 역할 설계 개요

| 계정 | 역할 | 소속 그룹 |
|------|------|----------|
| agent-admin | 운영/관리, cron 실행 | agent-common, agent-core |
| agent-dev | 개발, monitor.sh 작성자 | agent-common, agent-core |
| agent-test | QA/테스트 | agent-common |

| 그룹 | 용도 |
|------|------|
| agent-common | 공유 디렉토리(upload_files) 접근 |
| agent-core | 보안 디렉토리(api_keys, 로그) 접근 |

### 4-1. 그룹 생성 (계정보다 먼저)

```bash
sudo groupadd agent-common
sudo groupadd agent-core

# 생성 확인
grep "agent-" /etc/group
```

### 4-2. 계정 생성

```bash
# -m: 홈 디렉토리 자동 생성  -s /bin/bash: bash 셸 사용
sudo useradd -m -s /bin/bash agent-admin
sudo useradd -m -s /bin/bash agent-dev
sudo useradd -m -s /bin/bash agent-test
```

### 4-3. 비밀번호 설정

```bash
sudo passwd agent-admin   # 비밀번호 입력 (예: Admin1234)
sudo passwd agent-dev     # 비밀번호 입력
sudo passwd agent-test    # 비밀번호 입력
```

### 4-4. 그룹에 계정 추가

```bash
# agent-common 그룹에 3개 계정 추가
sudo usermod -aG agent-common agent-admin
sudo usermod -aG agent-common agent-dev
sudo usermod -aG agent-common agent-test

# agent-core 그룹에 2개 계정 추가
sudo usermod -aG agent-core agent-admin
sudo usermod -aG agent-core agent-dev

# agent-admin에 sudo 권한 부여 (관리 작업용)
sudo usermod -aG sudo agent-admin
```

> **`-aG` 주의:** `-a` 없이 `-G`만 쓰면 기존 그룹이 모두 제거됩니다. 반드시 `-aG`를 함께 사용하세요.

### 4-5. 그룹 소속 확인

```bash
id agent-admin
id agent-dev
id agent-test
```

**기대 출력:**
```
# agent-admin: agent-common, agent-core, sudo 포함
uid=1000(agent-admin) gid=XXXX(agent-admin) groups=...,agent-common,agent-core,sudo

# agent-dev: agent-common, agent-core 포함
uid=1001(agent-dev) gid=XXXX(agent-dev) groups=...,agent-common,agent-core

# agent-test: agent-common만 포함
uid=1002(agent-test) gid=XXXX(agent-test) groups=...,agent-common
```

---

## 5단계: 디렉토리 구조 및 권한 설정

### 5-1. 디렉토리 생성

```bash
# 앱 디렉토리 구조 생성
sudo mkdir -p /home/agent-admin/agent-app/upload_files
sudo mkdir -p /home/agent-admin/agent-app/api_keys
sudo mkdir -p /home/agent-admin/agent-app/bin

# 로그 디렉토리 생성
sudo mkdir -p /var/log/agent-app
```

### 5-2. 소유자/그룹 설정

```bash
# agent-app 전체 소유자를 agent-admin으로 설정
sudo chown -R agent-admin:agent-admin /home/agent-admin/agent-app

# upload_files: 그룹을 agent-common으로 (모두 공유)
sudo chown agent-admin:agent-common /home/agent-admin/agent-app/upload_files

# api_keys: 그룹을 agent-core로 (보안 디렉토리)
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: 그룹을 agent-core로
sudo chown agent-admin:agent-core /var/log/agent-app
```

### 5-3. 권한(Permission) 설정

```
리눅스 권한 숫자 표:
7 (rwx) = 읽기(4) + 쓰기(2) + 실행(1)
5 (r-x) = 읽기(4) + 실행(1)
0 (---) = 접근 불가
```

```bash
# upload_files: setgid(2) + 소유자rwx + 그룹rwx + 외부 차단
sudo chmod 2775 /home/agent-admin/agent-app/upload_files

# api_keys: 소유자rwx + 그룹r-x + 외부 차단
sudo chmod 750 /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: 소유자rwx + 그룹rwx + 외부 차단
sudo chmod 770 /var/log/agent-app
```

### 5-4. ACL(세밀한 권한) 설정

ACL은 기본 권한보다 더 정밀하게 특정 그룹/사용자 권한을 제어합니다.

```bash
# upload_files: agent-common 그룹 읽기/쓰기/실행 허용
sudo setfacl -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files
# 새로 만들어지는 파일에도 자동 적용 (default ACL)
sudo setfacl -d -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files

# api_keys: agent-core 그룹만 접근 허용
sudo setfacl -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys
sudo setfacl -d -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys

# /var/log/agent-app: agent-core 그룹 읽기/쓰기 허용
sudo setfacl -m g:agent-core:rwx /var/log/agent-app
sudo setfacl -d -m g:agent-core:rwx /var/log/agent-app
```

### 5-5. 권한 확인

```bash
# 일반 권한 확인 (sudo 필요)
sudo ls -la /home/agent-admin/agent-app/

# ACL 상세 확인
sudo getfacl /home/agent-admin/agent-app/upload_files
sudo getfacl /home/agent-admin/agent-app/api_keys
getfacl /var/log/agent-app
```

**`/var/log/agent-app` ACL 기대 출력:**
```
# file: var/log/agent-app
# owner: agent-admin
# group: agent-core
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
```

---

## 6단계: 앱 실행 환경 구성

### 6-1. agent-admin 계정으로 전환

```bash
su - agent-admin
# 비밀번호 입력
```

프롬프트가 `agent-admin@b1-lab:~$` 로 바뀝니다.

### 6-2. 앱 바이너리 배치

```bash
# /tmp에서 agent-app 디렉토리로 복사
cp /tmp/agent-app-linux-x86 /home/agent-admin/agent-app/
chmod +x /home/agent-admin/agent-app/agent-app-linux-x86
```

### 6-3. 키 파일 생성

```bash
# api_keys 디렉토리에 키 파일 생성
echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/t_secret.key

# 보안을 위해 소유자만 읽기 가능하도록 설정
chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key

# 내용 확인
cat /home/agent-admin/agent-app/api_keys/t_secret.key
```

**기대 출력:** `agent_api_key_test`

### 6-4. 환경 변수 설정

환경 변수는 프로그램이 실행 시 참조하는 설정값입니다. `.bashrc`에 넣으면 로그인할 때마다 자동 적용됩니다.

```bash
# agent-admin의 .bashrc에 환경 변수 추가
cat >> /home/agent-admin/.bashrc << 'EOF'

# ===== Agent 환경 변수 =====
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
export AGENT_LOG_DIR=/var/log/agent-app
EOF

# 즉시 적용
source /home/agent-admin/.bashrc

# 확인
echo "AGENT_HOME  : $AGENT_HOME"
echo "AGENT_PORT  : $AGENT_PORT"
echo "AGENT_KEY   : $AGENT_KEY_PATH"
echo "AGENT_LOG   : $AGENT_LOG_DIR"
```

**기대 출력:**
```
AGENT_HOME  : /home/agent-admin/agent-app
AGENT_PORT  : 15034
AGENT_KEY   : /home/agent-admin/agent-app/api_keys/t_secret.key
AGENT_LOG   : /var/log/agent-app
```

---

## 7단계: 앱 실행 확인

### 7-1. 앱 실행 (agent-admin 계정으로)

```bash
# agent-admin 계정으로 전환되어 있어야 합니다
cd /home/agent-admin/agent-app
./agent-app-linux-x86
```

### 7-2. 성공 출력 확인

아래와 같이 **5단계 모두 [OK]** 이고 마지막에 **"Agent READY"** 가 출력되어야 합니다:

```
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [OK]
   ... Verified key file with correct key string.
[4/5] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
```

> ❌ **[FAIL]이 나오면?**  
> - `[1/5]`: `whoami` 로 agent-admin인지 확인  
> - `[2/5]`: `source ~/.bashrc` 후 재실행  
> - `[3/5]`: `cat $AGENT_KEY_PATH` 내용이 `agent_api_key_test`인지 확인  
> - `[4/5]`: `ss -tulnp | grep 15034` 로 포트 사용 여부 확인  
> - `[5/5]`: `/var/log/agent-app` 권한 확인  

### 7-3. 새 터미널에서 포트 확인

앱이 실행 중인 상태에서, **새 터미널**을 열어 확인합니다.

**새 macOS 터미널 → orb shell b1-lab:**
```bash
ss -tulnp | grep 15034
```

**기대 출력:**
```
tcp  LISTEN  0  1  0.0.0.0:15034  0.0.0.0:*
```

### 7-4. 앱을 백그라운드로 실행 (cron 테스트용)

```bash
# 앱을 실행 중인 터미널에서 Ctrl+C로 종료 후
# 백그라운드로 실행 (crontab 테스트 시 필요)
nohup /home/agent-admin/agent-app/agent-app-linux-x86 > /tmp/agent-app.log 2>&1 &

# 실행 확인
pgrep -f "agent-app-linux-x86"
```

---

## 8단계: monitor.sh 작성

### 왜 모니터링 스크립트가 필요한가요?
서버는 24시간 운영됩니다. 자동으로 상태를 수집하고 로그로 남기면 나중에 "언제부터 문제가 생겼는지" 추적할 수 있습니다.

### 8-1. 스크립트 파일 생성

**agent-admin 계정에서 (또는 sudo):**

```bash
# bin 디렉토리로 이동
cd /home/agent-admin/agent-app/bin

# nano 편집기로 파일 생성
nano monitor.sh
```

아래 내용을 **전체** 복사하여 붙여넣기 합니다 (`Ctrl+Shift+V` 또는 마우스 우클릭):

```bash
#!/bin/bash
# =============================================================
# monitor.sh - 시스템 관제 자동화 스크립트
# 소유자: agent-dev  그룹: agent-core  권한: 750
# 실행자: agent-admin (agent-core 그룹 소속)
# =============================================================

# ---- 설정값 ----
APP_PROCESS="agent-app-linux-x86"          # 감시할 프로세스 이름
APP_PORT=15034                              # 감시할 포트 번호
LOG_FILE="/var/log/agent-app/monitor.log"  # 로그 파일 경로
MAX_LOG_SIZE=$((10 * 1024 * 1024))         # 최대 로그 크기: 10MB
MAX_LOG_FILES=10                            # 최대 로그 파일 개수

# ---- 임계값 ----
CPU_THRESHOLD=20
MEM_THRESHOLD=10
DISK_THRESHOLD=80

# ---- 로그 로테이션 함수 ----
rotate_log() {
    if [ ! -f "$LOG_FILE" ]; then
        return
    fi
    local size
    size=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$size" -ge "$MAX_LOG_SIZE" ]; then
        for i in $(seq $((MAX_LOG_FILES - 1)) -1 1); do
            [ -f "${LOG_FILE}.$i" ] && mv "${LOG_FILE}.$i" "${LOG_FILE}.$((i + 1))"
        done
        mv "$LOG_FILE" "${LOG_FILE}.1"
        touch "$LOG_FILE"
    fi
}

# ---- 현재 시각 ----
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""

# =============================================================
# [1] HEALTH CHECK - 프로세스 및 포트 확인
# =============================================================
echo "[HEALTH CHECK]"

# 프로세스 확인 (비정상 시 exit 1)
PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    echo "Checking process '$APP_PROCESS'... [FAIL] Process not running!"
    exit 1
else
    echo "Checking process '$APP_PROCESS'... [OK] (PID: $PID)"
fi

# 포트 확인 (비정상 시 exit 1)
PORT_STATUS=$(ss -tulnp 2>/dev/null | grep ":${APP_PORT} ")
if [ -z "$PORT_STATUS" ]; then
    echo "Checking port $APP_PORT... [FAIL] Port not listening!"
    exit 1
else
    echo "Checking port $APP_PORT... [OK]"
fi

echo ""

# =============================================================
# [2] 방화벽 상태 점검 (경고만, 종료 안 함)
# =============================================================
echo "[FIREWALL CHECK]"

# systemctl로 UFW 상태 확인 (sudo 불필요)
if systemctl is-active --quiet ufw 2>/dev/null; then
    echo "Firewall (UFW)... [OK] Active"
else
    echo "[WARNING] Firewall (UFW) is not active!"
fi

echo ""

# =============================================================
# [3] RESOURCE MONITORING - CPU / MEM / DISK 수집
# =============================================================
echo "[RESOURCE MONITORING]"

# CPU 사용률 수집
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")

# 메모리 사용률 수집
MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
MEM_USED=$(free | grep Mem | awk '{print $3}')
if [ "${MEM_TOTAL:-0}" -gt 0 ]; then
    MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEM_USAGE="0.0"
fi

# 디스크 사용률 수집 (루트 파티션)
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""

# =============================================================
# [4] 임계값 경고 (경고만, 종료 안 함)
# =============================================================
CPU_INT=$(echo "$CPU_USAGE" | cut -d'.' -f1)
if [ "${CPU_INT:-0}" -gt "$CPU_THRESHOLD" ]; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
fi

MEM_INT=$(echo "$MEM_USAGE" | cut -d'.' -f1)
if [ "${MEM_INT:-0}" -gt "$MEM_THRESHOLD" ]; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
fi

if [ "${DISK_USAGE:-0}" -gt "$DISK_THRESHOLD" ]; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"
fi

echo ""
echo "===================================="

# =============================================================
# [5] 로그 기록
# =============================================================

# 로그 디렉토리 없으면 생성
LOG_DIR=$(dirname "$LOG_FILE")
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR" 2>/dev/null
fi

# 로그 로테이션 실행 (10MB 초과 시 자동 순환)
rotate_log

# 로그 한 줄 추가 기록 (>> : 누적 기록)
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

### 8-2. 소유자 및 권한 설정

**sudo 권한이 있는 계정에서:**

```bash
# 소유자: agent-dev, 그룹: agent-core
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh

# 권한 750: 소유자(rwx), 그룹(r-x), 기타(--)
sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh

# 확인
sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
```

**기대 출력:**
```
-rwxr-x--- 1 agent-dev agent-core XXXX monitor.sh
```

```
권한 해석:
-rwxr-x---
 ├─rwx : agent-dev (소유자) → 읽기+쓰기+실행 ✅
 ├─r-x : agent-core (그룹)  → 읽기+실행     ✅ (agent-admin이 속함)
 └─--- : 기타               → 접근 불가     ✅
```

### 8-3. 스크립트 테스트 실행

앱이 실행 중인 상태에서:

```bash
# agent-admin 계정으로 전환 후 실행
su - agent-admin
/home/agent-admin/agent-app/bin/monitor.sh
```

**정상 출력 예시:**
```
====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 1312)
Checking port 15034... [OK]

[FIREWALL CHECK]
Firewall (UFW)... [OK] Active

[RESOURCE MONITORING]
CPU Usage  : 2.5%
MEM Usage  : 4.8%
DISK Used  : 1%

====================================
[INFO] Log appended: /var/log/agent-app/monitor.log
```

### 8-4. 로그 확인

```bash
cat /var/log/agent-app/monitor.log
```

**기대 출력:**
```
[2026-05-26 10:30:01] PID:1312 CPU:2.5% MEM:4.8% DISK_USED:1%
```

---

## 9단계: cron을 위한 sudo NOPASSWD 설정

cron은 터미널 없이(비대화식으로) 실행되므로, `sudo` 명령에 비밀번호 없이 실행 가능하도록 설정해야 합니다.

```bash
# visudo로 sudoers 파일 편집 (직접 편집하면 시스템이 망가질 수 있으므로 반드시 visudo 사용)
sudo visudo
```

파일 맨 아래에 추가:
```
# agent-admin이 패스워드 없이 ufw status 실행 가능
agent-admin ALL=(ALL) NOPASSWD: /usr/sbin/ufw status, /usr/sbin/ufw *
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## 10단계: crontab 자동 실행 등록

### crontab이란?
정해진 시간에 자동으로 명령을 실행하는 리눅스 스케줄러입니다.

```
* * * * *  실행할_명령어
│ │ │ │ │
│ │ │ │ └─ 요일 (0=일, 6=토)
│ │ │ └─── 월 (1-12)
│ │ └───── 일 (1-31)
│ └─────── 시 (0-23)
└───────── 분 (0-59)
```
`* * * * *` = **매분 실행**

### 10-1. agent-admin crontab 등록

```bash
# agent-admin 계정으로 전환
su - agent-admin

# crontab 편집기 열기
crontab -e
```

처음 실행 시 편집기 선택 → **1번 (nano)** 선택

파일 맨 아래에 아래 줄 추가:
```
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

### 10-2. crontab 등록 확인

```bash
crontab -l
```

마지막 줄에 추가한 내용이 보여야 합니다.

### 10-3. cron 서비스 확인

```bash
sudo systemctl status cron
```

`active (running)` 상태여야 합니다. 아니라면:
```bash
sudo systemctl start cron
sudo systemctl enable cron
```

### 10-4. 1~2분 후 자동 실행 확인

```bash
# 실시간 로그 모니터링 (새 줄이 매분 추가되는 것 확인)
tail -f /var/log/agent-app/monitor.log
```

1분마다 새 줄이 추가되는 것을 확인했으면 `Ctrl+C`로 종료합니다.

**기대 출력:**
```
[2026-05-26 10:30:01] PID:1312 CPU:2.5% MEM:4.8% DISK_USED:1%
[2026-05-26 10:31:01] PID:1312 CPU:3.1% MEM:4.9% DISK_USED:1%
[2026-05-26 10:32:01] PID:1312 CPU:2.8% MEM:5.0% DISK_USED:1%
```

---

## 11단계: 최종 검증 체크리스트

수행 내역서 제출 전 아래 명령어를 모두 실행하고 결과를 캡처하세요.

```bash
# ✅ 1. SSH 포트 변경 확인
grep -E "^Port|^PermitRootLogin" /etc/ssh/sshd_config
# 기대: Port 20022 / PermitRootLogin no

# ✅ 2. SSH 포트 리슨 확인
sudo ss -tulnp | grep sshd
# 기대: 0.0.0.0:20022 ... sshd

# ✅ 3. 방화벽 규칙 확인
sudo ufw status
# 기대: 20022/tcp ALLOW, 15034/tcp ALLOW

# ✅ 4. 계정 그룹 소속 확인
id agent-admin && id agent-dev && id agent-test
# agent-admin: sudo, agent-common, agent-core 포함
# agent-dev: agent-common, agent-core 포함
# agent-test: agent-common만 포함

# ✅ 5. 디렉토리 권한 확인
sudo ls -la /home/agent-admin/agent-app/
sudo ls -la /var/log/agent-app

# ✅ 6. ACL 권한 확인
sudo getfacl /home/agent-admin/agent-app/upload_files
sudo getfacl /home/agent-admin/agent-app/api_keys
getfacl /var/log/agent-app

# ✅ 7. 키 파일 내용 확인
sudo cat /home/agent-admin/agent-app/api_keys/t_secret.key
# 기대: agent_api_key_test

# ✅ 8. 환경 변수 확인 (agent-admin 계정으로)
su - agent-admin -c "echo AGENT_HOME=\$AGENT_HOME && echo AGENT_PORT=\$AGENT_PORT"
# 기대: AGENT_HOME=/home/agent-admin/agent-app, AGENT_PORT=15034

# ✅ 9. 앱 프로세스 및 포트 확인 (앱이 실행 중이어야 함)
pgrep -f "agent-app-linux-x86" && ss -tulnp | grep 15034

# ✅ 10. monitor.sh 권한 확인
sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
# 기대: -rwxr-x--- 1 agent-dev agent-core

# ✅ 11. crontab 등록 확인
su - agent-admin -c "crontab -l"
# 기대: * * * * * /home/agent-admin/agent-app/bin/monitor.sh ...

# ✅ 12. 로그 누적 확인
tail -20 /var/log/agent-app/monitor.log
# 기대: 매분 한 줄씩 기록된 로그
```

### 스크린샷 목록 (수행 내역서 첨부용)

| 번호 | 캡처 내용 |
|------|----------|
| 1 | `grep -E "^Port\|^PermitRootLogin" /etc/ssh/sshd_config` 출력 |
| 2 | `sudo ss -tulnp \| grep sshd` 출력 |
| 3 | `sudo ufw status` 출력 |
| 4 | `id agent-admin && id agent-dev && id agent-test` 출력 |
| 5 | `sudo ls -la /home/agent-admin/agent-app/` 출력 |
| 6 | `getfacl /var/log/agent-app` 출력 |
| 7 | 앱 Boot Sequence 터미널 전체 출력 (`Agent READY` 포함) |
| 8 | `monitor.sh` 실행 결과 전체 |
| 9 | `tail -20 /var/log/agent-app/monitor.log` (누적 로그) |
| 10 | `crontab -l` 출력 |

---

## 보너스 과제

### 보너스 1: report.sh (로그 통계 리포트)

```bash
nano /home/agent-admin/agent-app/bin/report.sh
```

```bash
#!/bin/bash
# =============================================================
# report.sh - monitor.log 통계 분석 리포트
# 사용법: ./report.sh [시작시간] [종료시간]
# 예시:   ./report.sh "2026-05-26 10:00:00" "2026-05-26 11:00:00"
# =============================================================

LOG_FILE="/var/log/agent-app/monitor.log"
START_TIME="$1"
END_TIME="$2"

if [ ! -f "$LOG_FILE" ]; then
    echo "[ERROR] 로그 파일 없음: $LOG_FILE"
    exit 1
fi

# 시간 범위 필터링
if [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
    LOG_DATA=$(awk -v s="[$START_TIME" -v e="[$END_TIME" '$0 >= s && $0 <= e' "$LOG_FILE")
    echo "분석 범위: $START_TIME ~ $END_TIME"
else
    LOG_DATA=$(cat "$LOG_FILE")
    echo "분석 범위: 전체 로그"
fi

if [ -z "$LOG_DATA" ]; then
    echo "[WARNING] 분석할 데이터가 없습니다."
    exit 0
fi

# AWK로 통계 계산
echo "$LOG_DATA" | awk '
{
    match($0, /CPU:([0-9.]+)%/, c);   cpu  = c[1] + 0
    match($0, /MEM:([0-9.]+)%/, m);   mem  = m[1] + 0
    match($0, /DISK_USED:([0-9.]+)%/, d); disk = d[1] + 0
    match($0, /\[([0-9-]+ [0-9:]+)\]/, t); ts = t[1]

    cpu_sum += cpu; mem_sum += mem; disk_sum += disk; count++

    if (count == 1 || cpu  > cpu_max)  { cpu_max  = cpu;  cpu_max_ts  = ts }
    if (count == 1 || cpu  < cpu_min)  { cpu_min  = cpu;  cpu_min_ts  = ts }
    if (count == 1 || mem  > mem_max)  { mem_max  = mem;  mem_max_ts  = ts }
    if (count == 1 || mem  < mem_min)  { mem_min  = mem;  mem_min_ts  = ts }
    if (count == 1 || disk > disk_max) { disk_max = disk; disk_max_ts = ts }
    if (count == 1 || disk < disk_min) { disk_min = disk; disk_min_ts = ts }
}
END {
    if (count == 0) { print "[WARNING] 데이터 없음"; exit }
    printf "\n    ====== STATISTICS REPORT ======\n"
    printf "      [CPU]\n"
    printf "        Average : %.1f%%\n",        cpu_sum  / count
    printf "        Maximum : %.1f%% at %s\n",  cpu_max,  cpu_max_ts
    printf "        Minimum : %.1f%% at %s\n",  cpu_min,  cpu_min_ts
    printf "      [Memory]\n"
    printf "        Average : %.1f%%\n",        mem_sum  / count
    printf "        Maximum : %.1f%% at %s\n",  mem_max,  mem_max_ts
    printf "        Minimum : %.1f%% at %s\n",  mem_min,  mem_min_ts
    printf "      [Disk]\n"
    printf "        Average : %.1f%%\n",        disk_sum / count
    printf "        Maximum : %.1f%% at %s\n",  disk_max, disk_max_ts
    printf "        Minimum : %.1f%% at %s\n",  disk_min, disk_min_ts
    printf "      [Samples]\n"
    printf "        Data Points: %d samples\n\n", count
}
'
```

```bash
# 권한 설정
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/report.sh
sudo chmod 750 /home/agent-admin/agent-app/bin/report.sh

# 실행 (전체 로그 분석)
su - agent-admin -c "/home/agent-admin/agent-app/bin/report.sh"

# 실행 (시간 범위 지정)
su - agent-admin -c '/home/agent-admin/agent-app/bin/report.sh "2026-05-26 10:00:00" "2026-05-26 11:00:00"'
```

---

### 보너스 2: log_archive.sh (시간 기반 로그 보존 정책)

```bash
nano /home/agent-admin/agent-app/bin/log_archive.sh
```

```bash
#!/bin/bash
# =============================================================
# log_archive.sh - 시간 기반 로그 보존 정책
# - 7일 경과 로그 압축 → /var/log/monitor/agent-app/archive/ 이동
# - 30일 경과 아카이브 삭제
# =============================================================

LOG_DIR="/var/log/agent-app"
ARCHIVE_DIR="/var/log/monitor/agent-app/archive"

# ---- 아카이브 디렉토리 생성 ----
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[ERROR] 아카이브 디렉토리 생성 실패: $ARCHIVE_DIR (권한 부족)"
        exit 1
    fi
    echo "[INFO] 아카이브 디렉토리 생성: $ARCHIVE_DIR"
fi

# ---- 로그 디렉토리 존재 확인 ----
if [ ! -d "$LOG_DIR" ]; then
    echo "[ERROR] 로그 디렉토리 없음: $LOG_DIR"
    exit 1
fi

# ---- 7일 경과 로그 압축 → 아카이브 이동 ----
echo "[INFO] 7일 경과 로그 압축 중..."
OLD_FILES=$(find "$LOG_DIR" -name "*.log" -mtime +7 2>/dev/null)

if [ -z "$OLD_FILES" ]; then
    echo "[INFO] 압축 대상 없음 (7일 이내 로그만 존재)"
else
    echo "$OLD_FILES" | while IFS= read -r file; do
        BASENAME=$(basename "$file")
        DEST="${ARCHIVE_DIR}/${BASENAME}.$(date +%Y%m%d).gz"
        if gzip -c "$file" > "$DEST" 2>/dev/null; then
            rm -f "$file"
            echo "[OK] 압축/이동: $file → $DEST"
        else
            echo "[WARNING] 압축 실패: $file"
        fi
    done
fi

# ---- 30일 경과 아카이브 삭제 ----
echo "[INFO] 30일 경과 아카이브 삭제 중..."
OLD_ARCHIVES=$(find "$ARCHIVE_DIR" -name "*.gz" -mtime +30 2>/dev/null)

if [ -z "$OLD_ARCHIVES" ]; then
    echo "[INFO] 삭제 대상 없음 (30일 이내 아카이브만 존재)"
else
    echo "$OLD_ARCHIVES" | while IFS= read -r archive; do
        rm -f "$archive"
        echo "[OK] 삭제: $archive"
    done
fi

echo "[INFO] 로그 보존 정책 완료"
```

```bash
# 권한 설정
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/bin/log_archive.sh
sudo chmod 750 /home/agent-admin/agent-app/bin/log_archive.sh

# 아카이브 디렉토리 권한 설정
sudo mkdir -p /var/log/monitor/agent-app/archive
sudo chown agent-admin:agent-core /var/log/monitor/agent-app/archive
sudo chmod 770 /var/log/monitor/agent-app/archive

# 테스트 실행
su - agent-admin -c "/home/agent-admin/agent-app/bin/log_archive.sh"

# crontab에 매일 새벽 2시 등록
su - agent-admin
crontab -e
# 아래 줄 추가:
# 0 2 * * * /home/agent-admin/agent-app/bin/log_archive.sh >> /var/log/agent-app/archive.log 2>&1
```

---

## ⚠️ 자주 발생하는 문제 해결

### Q1. `ls -la /home/agent-admin/agent-app/` → Permission denied
```bash
# 이유: 다른 계정에서 agent-admin 홈 디렉토리 접근 불가
# 해결: sudo 사용
sudo ls -la /home/agent-admin/agent-app/
```

### Q2. monitor.sh 실행 시 "Permission denied"
```bash
# 실행 권한 및 계정 확인
ls -l /home/agent-admin/agent-app/bin/monitor.sh
whoami   # agent-admin이어야 함
id agent-admin   # agent-core 그룹 소속 확인
```

### Q3. 로그에 기록이 안 됨
```bash
# /var/log/agent-app 쓰기 권한 테스트
su - agent-admin -c "echo test >> /var/log/agent-app/monitor.log && echo OK"

# 권한 재확인
ls -la /var/log/agent-app
getfacl /var/log/agent-app
```

### Q4. cron이 실행되지 않음
```bash
# cron 서비스 확인
sudo systemctl status cron

# cron 로그 확인
grep CRON /var/log/syslog | tail -20

# 앱이 실행 중인지 확인 (앱이 꺼지면 health check 실패로 exit 1)
pgrep -f "agent-app-linux-x86"
```

### Q5. 앱 실행 시 `[3/5] Checking Required Files [FAIL]`
```bash
# 키 파일 내용 확인 (공백/개행 없이 정확히 "agent_api_key_test")
cat -A /home/agent-admin/agent-app/api_keys/t_secret.key
# 이상하면 다시 생성
printf "agent_api_key_test\n" > /home/agent-admin/agent-app/api_keys/t_secret.key
```

### Q6. `>> vs >` 차이
```
>  : 덮어쓰기 (파일 내용 초기화 후 기록)
>> : 누적 쓰기 (파일 끝에 이어서 기록)

로그는 반드시 >> 사용!
monitor.log에 > 를 쓰면 이전 기록이 모두 사라집니다.
```

---

## 📚 핵심 개념 요약

| 개념 | 설명 |
|------|------|
| SSH 포트 변경 | 기본 22번 대신 20022 사용 → 자동화 공격 회피 |
| Root 접속 차단 | 루트 직접 로그인 금지 → 비밀번호 유출 시 피해 최소화 |
| 방화벽 (UFW) | 필요한 포트(20022, 15034)만 허용 → 공격 면 최소화 |
| 최소 권한 원칙 | 각 역할에 필요한 최소한의 권한만 부여 |
| ACL | 기본 권한(chmod)을 넘어선 세밀한 접근 제어 |
| crontab | `* * * * *` = 매분, `0 2 * * *` = 매일 새벽 2시 |
| 로그 로테이션 | 로그 파일이 무한 증가하지 않도록 순환/압축/삭제 |
| exit 1 vs 경고 | 치명적 오류(프로세스/포트 다운) → exit 1, 주의 사항 → WARNING만 출력 |

---

> **완료 후:** [11단계 체크리스트](#11단계-최종-검증-체크리스트)의 모든 명령 결과를 캡처하여 수행 내역서에 첨부하세요.
