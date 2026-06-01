# B1-1 미션 교본 — 시스템 관제 자동화 스크립트 개발

> **대상:** 리눅스 입문자 (처음 서버를 다루는 분)
> **환경:** macOS + OrbStack + Ubuntu 22.04
> **학습 시간:** 약 40시간 (실습 포함)

---

## 1. 이 미션은 무엇인가요?

### 한 줄 요약
> "실제 서버 엔지니어처럼 리눅스 서버를 구축하고, 자동으로 상태를 감시하는 스크립트를 만든다."

### 왜 이 미션이 중요한가요?

서버를 운영하다 보면 이런 상황이 생깁니다:
- 새벽에 갑자기 서버가 다운됨 → "언제부터? 왜?" → 로그가 없으면 **감**에 의존
- 해커가 22번 포트(기본 SSH)로 계속 공격 → 포트를 바꾸지 않으면 위험
- 여러 팀원이 같은 서버를 사용 → 권한 관리가 없으면 실수로 중요 파일 삭제

이 미션은 이런 실제 문제를 직접 해결하는 경험을 제공합니다.

### 미션이 끝나면 할 수 있는 것

| 할 수 있는 것 | 왜 중요한가 |
|---|---|
| SSH 포트 변경 및 보안 설정 | 기본 보안의 첫 번째 단계 |
| 방화벽으로 필요한 포트만 열기 | 공격 면 최소화 |
| 역할별 계정/그룹으로 권한 분리 | 실수와 보안 사고 예방 |
| 앱 실행 환경 구성 | 안정적인 서비스 운영 |
| 자동 모니터링 스크립트 작성 | 문제를 데이터로 기록하여 추적 |
| crontab으로 자동화 | 사람 없이도 주기적으로 실행 |

---

## 2. 환경 설정 (처음 한 번만)

### 2-1. OrbStack 설치

OrbStack은 Mac에서 리눅스 가상 환경을 쉽게 만들 수 있는 도구입니다.

```
https://orbstack.dev → Download → 설치
```

설치 후 상단 메뉴바에 OrbStack 아이콘이 생기면 성공입니다.

### 2-2. Ubuntu 가상 머신 생성

**OrbStack 앱 → Machines → New Machine:**

| 항목 | 값 |
|---|---|
| 이름 | b1-lab |
| OS | Ubuntu 22.04 |
| CPU/Memory | 기본값 |

또는 터미널에서:
```bash
# macOS 터미널에서 실행
orb create ubuntu:22.04 b1-lab
```

### 2-3. 가상 머신 접속

```bash
# macOS 터미널에서 실행
orb shell b1-lab
```

접속 성공 시 프롬프트가 바뀝니다:
```
ubuntu@b1-lab:~$
```

### 2-4. 필수 패키지 설치

```bash
# VM 안에서 실행
sudo apt update                        # 패키지 목록 최신화
sudo apt install -y acl ufw net-tools  # 필요한 도구 설치
# acl: 세밀한 권한 제어 도구
# ufw: 방화벽 도구
# net-tools: 네트워크 확인 도구
```

### 2-5. 앱 파일을 VM으로 복사

```bash
# macOS 터미널(새 창)에서 실행 — orb shell 밖에서!
orb push b1-lab \
  /Users/cspag5955/OrbStack/AI-SW-ubuntu24/home/cspag5955/AI-SW-Basic/b1-1/실행파일/agent-app-linux-x86 \
  /tmp/agent-app-linux-x86
```

> **팁:** OrbStack은 Mac 파일을 VM 안에서 `/mac/Users/사용자명/` 경로로 바로 접근할 수도 있습니다.

---

## 3. 전체 과제 흐름

```
[준비]
  OrbStack 설치 → Ubuntu VM 생성 → 패키지 설치 → 앱 파일 복사
       ↓
[보안 설정]
  1단계: SSH 포트 변경 (22 → 20022) + Root 원격 접속 차단
       ↓
  2단계: 방화벽(UFW) 설정 → 20022, 15034 포트만 허용
       ↓
[계정/권한 설정]
  3단계: 그룹 생성 (agent-common, agent-core)
       ↓
  4단계: 계정 생성 (agent-admin, agent-dev, agent-test)
       ↓
  5단계: 디렉토리 생성 + 권한/ACL 설정
       ↓
[앱 실행 환경]
  6단계: 환경 변수 설정 (.bashrc에 등록)
       ↓
  7단계: 키 파일 생성 + 앱 실행 → Boot Sequence 5단계 [OK] 확인
       ↓
[자동화]
  8단계: monitor.sh 작성 (프로세스/포트/CPU/메모리/디스크 감시)
       ↓
  9단계: crontab 등록 → 매분 자동 실행
       ↓
[검증]
  10단계: 최종 체크리스트 확인 + 스크린샷 캡처
```

---

## 4. 단계별 따라하기

### 1단계 — SSH 보안 설정

**왜 하나요?**
SSH 기본 포트 22번은 전 세계 해커의 자동화 공격이 집중됩니다.
Root 원격 접속을 차단하면 비밀번호가 유출되어도 서버 장악을 막을 수 있습니다.

```bash
# SSH 설정 파일 열기
sudo nano /etc/ssh/sshd_config

# 아래 두 줄을 찾아서 수정:
#   #Port 22                        → Port 20022
#   #PermitRootLogin prohibit-password  → PermitRootLogin no
#
# nano 단축키: Ctrl+W(검색) Ctrl+O(저장) Ctrl+X(종료)

# SSH 서비스 재시작 (설정 적용)
sudo systemctl restart sshd

# 확인 — 아래 두 줄이 보여야 함
grep -E "^Port|^PermitRootLogin" /etc/ssh/sshd_config
# 기대 출력:
# Port 20022
# PermitRootLogin no

# 실제 포트 리슨 확인
sudo ss -tulnp | grep sshd
# 기대 출력: ... 0.0.0.0:20022 ... sshd
```

> **OrbStack 참고:** `orb shell` 접속은 SSH와 별개라 포트 변경 후에도 정상 접속됩니다.

---

### 2단계 — 방화벽(UFW) 설정

**왜 하나요?**
서버의 "문지기" 역할입니다. SSH(20022)와 앱(15034) 포트만 열고 나머지는 모두 차단합니다.

> **⚠️ 중요:** 포트 허용을 먼저 하고 enable 하세요. 순서를 바꾸면 접속이 차단됩니다!

```bash
# 1. SSH 포트 먼저 허용 (순서 중요!)
sudo ufw allow 20022/tcp

# 2. 앱 포트 허용
sudo ufw allow 15034/tcp

# 3. UFW 활성화 (y 입력)
sudo ufw enable

# 4. 확인
sudo ufw status
# 기대 출력:
# Status: active
# 20022/tcp    ALLOW    Anywhere
# 15034/tcp    ALLOW    Anywhere
```

---

### 3단계 — 그룹 생성

**왜 하나요?**
그룹은 "팀" 개념입니다. 팀별로 접근할 수 있는 디렉토리를 구분하기 위해 먼저 만들어야 합니다.

| 그룹 | 역할 |
|---|---|
| agent-common | 공유 파일(upload_files) 접근 가능 — admin, dev, test 모두 |
| agent-core | 보안 파일(api_keys, 로그) 접근 가능 — admin, dev만 |

```bash
# 그룹 생성
sudo groupadd agent-common
sudo groupadd agent-core

# 생성 확인
grep "agent-" /etc/group
# 기대: agent-common:x:XXXX:   와   agent-core:x:XXXX:  가 보여야 함
```

---

### 4단계 — 계정 생성 및 그룹 배정

**왜 하나요?**
각자 역할에 맞는 최소한의 권한만 줘야 실수로 인한 사고를 막을 수 있습니다.

```bash
# 계정 생성 (-m: 홈 디렉토리 자동 생성, -s: bash 셸 사용)
sudo useradd -m -s /bin/bash agent-admin
sudo useradd -m -s /bin/bash agent-dev
sudo useradd -m -s /bin/bash agent-test

# 비밀번호 설정 (각각 입력)
sudo passwd agent-admin   # 예: Admin1234
sudo passwd agent-dev
sudo passwd agent-test

# 그룹 배정 (-aG: 기존 그룹 유지하면서 추가, -a 없으면 기존 그룹 삭제됨!)
sudo usermod -aG agent-common agent-admin   # admin → common 그룹 추가
sudo usermod -aG agent-common agent-dev     # dev   → common 그룹 추가
sudo usermod -aG agent-common agent-test    # test  → common 그룹 추가
sudo usermod -aG agent-core   agent-admin   # admin → core 그룹 추가
sudo usermod -aG agent-core   agent-dev     # dev   → core 그룹 추가
sudo usermod -aG sudo         agent-admin   # admin → sudo 권한 부여

# 확인
id agent-admin
# 기대: groups=...,agent-common,agent-core,sudo 포함

id agent-dev
# 기대: groups=...,agent-common,agent-core 포함

id agent-test
# 기대: groups=...,agent-common만 포함 (core 없음!)
```

---

### 5단계 — 디렉토리 구조 및 권한 설정

**왜 하나요?**
공유 디렉토리와 보안 디렉토리를 분리하여 필요한 사람만 접근하도록 합니다.

```bash
# 디렉토리 생성
sudo mkdir -p /home/agent-admin/agent-app/upload_files  # 공유 파일 보관
sudo mkdir -p /home/agent-admin/agent-app/api_keys      # 보안 키 파일
sudo mkdir -p /home/agent-admin/agent-app/bin           # 스크립트 보관
sudo mkdir -p /var/log/agent-app                        # 로그 저장

# 소유자 설정
sudo chown -R agent-admin:agent-admin /home/agent-admin/agent-app
sudo chown agent-admin:agent-common   /home/agent-admin/agent-app/upload_files  # 공유 디렉토리
sudo chown agent-admin:agent-core     /home/agent-admin/agent-app/api_keys      # 보안 디렉토리
sudo chown agent-admin:agent-core     /var/log/agent-app                        # 로그 디렉토리

# 권한 설정
# 숫자 의미: 7=읽기+쓰기+실행, 5=읽기+실행, 0=접근불가
# 2775 = setgid(2) + 소유자(7) + 그룹(7) + 외부(5)
sudo chmod 2775 /home/agent-admin/agent-app/upload_files  # 공유: 그룹 모두 읽기/쓰기
sudo chmod 750  /home/agent-admin/agent-app/api_keys      # 보안: 그룹만 읽기
sudo chmod 770  /var/log/agent-app                        # 로그: 그룹 읽기/쓰기

# ACL 설정 (더 세밀한 권한 제어)
# -m: 권한 추가, -d: 새로 만들어지는 파일에도 자동 적용
sudo setfacl -m  g:agent-common:rwx /home/agent-admin/agent-app/upload_files
sudo setfacl -d -m g:agent-common:rwx /home/agent-admin/agent-app/upload_files

sudo setfacl -m  g:agent-core:rwx /home/agent-admin/agent-app/api_keys
sudo setfacl -d -m g:agent-core:rwx /home/agent-admin/agent-app/api_keys

sudo setfacl -m  g:agent-core:rwx /var/log/agent-app
sudo setfacl -d -m g:agent-core:rwx /var/log/agent-app

# 확인
sudo ls -la /home/agent-admin/agent-app/
getfacl /var/log/agent-app
```

---

### 6단계 — 앱 실행 환경 구성

**왜 하나요?**
환경 변수를 사용하면 경로가 바뀌어도 변수 하나만 수정하면 됩니다. 유지보수가 쉬워집니다.

```bash
# agent-admin 계정으로 전환
su - agent-admin
# 비밀번호 입력 → 프롬프트가 agent-admin@b1-lab:~$ 로 바뀜

# 앱 파일 복사 및 실행 권한 부여
cp /tmp/agent-app-linux-x86 /home/agent-admin/agent-app/
chmod +x /home/agent-admin/agent-app/agent-app-linux-x86
# chmod +x: 실행 권한 추가 (없으면 ./앱이름 실행 불가)

# 키 파일 생성 (앱이 실행될 때 확인하는 인증 파일)
echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/t_secret.key
chmod 600 /home/agent-admin/agent-app/api_keys/t_secret.key
# chmod 600: 소유자만 읽기/쓰기 (보안 파일이므로 엄격하게 설정)

# 내용 확인 (정확히 agent_api_key_test 한 줄이어야 함)
cat /home/agent-admin/agent-app/api_keys/t_secret.key

# 환경 변수 등록 (.bashrc에 추가 → 로그인할 때마다 자동 적용)
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

# 확인 (모두 올바른 경로가 출력되어야 함)
echo "AGENT_HOME : $AGENT_HOME"
echo "AGENT_PORT : $AGENT_PORT"
echo "AGENT_KEY  : $AGENT_KEY_PATH"
echo "AGENT_LOG  : $AGENT_LOG_DIR"
```

---

### 7단계 — 앱 실행 및 확인

**왜 하나요?**
앱이 정상적으로 실행되는지 Boot Sequence 5단계를 통해 확인합니다. 하나라도 FAIL이면 설정이 잘못된 것입니다.

```bash
# agent-admin 계정에서 실행
cd /home/agent-admin/agent-app
./agent-app-linux-x86
```

**반드시 아래처럼 5단계 모두 [OK]가 나와야 합니다:**

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

**FAIL이 나오면?**

| 단계 | 원인 | 해결 |
|---|---|---|
| [1/5] FAIL | root나 다른 계정으로 실행 | `su - agent-admin` 후 재실행 |
| [2/5] FAIL | 환경 변수 미적용 | `source ~/.bashrc` 후 재실행 |
| [3/5] FAIL | 키 파일 내용 불일치 | `cat $AGENT_KEY_PATH` 확인, 재생성 |
| [4/5] FAIL | 15034 포트 사용 중 | `ss -tulnp \| grep 15034` 확인 |
| [5/5] FAIL | 로그 디렉토리 권한 없음 | `ls -la /var/log/agent-app` 확인 |

```bash
# 앱을 백그라운드로 실행 (monitor.sh 테스트를 위해 계속 켜둬야 함)
# 기존 앱 Ctrl+C로 종료 후:
nohup /home/agent-admin/agent-app/agent-app-linux-x86 > /tmp/agent-app.log 2>&1 &
# nohup: 터미널을 닫아도 계속 실행
# &: 백그라운드 실행
# > /tmp/agent-app.log: 출력을 파일로 저장

# 실행 확인
pgrep -f "agent-app-linux-x86"
# 숫자(PID)가 출력되면 실행 중
```

---

### 8단계 — monitor.sh 작성

**왜 하나요?**
서버 상태를 매분 자동으로 수집하고 기록해두면, 나중에 "언제 문제가 생겼는지" 로그로 확인할 수 있습니다.

```bash
# agent-admin 계정에서
mkdir -p /home/agent-admin/agent-app/bin
nano /home/agent-admin/agent-app/bin/monitor.sh
```

아래 내용을 전체 복사하여 붙여넣기 (`Ctrl+Shift+V`):

```bash
#!/bin/bash
# =============================================================
# monitor.sh - 시스템 관제 자동화 스크립트
# 소유자: agent-dev  그룹: agent-core  권한: 750
# =============================================================

# ---- 설정값 (필요 시 수정) ----
APP_PROCESS="agent-app-linux-x86"         # 감시할 프로세스 이름
APP_PORT=15034                            # 감시할 포트 번호
LOG_FILE="/var/log/agent-app/monitor.log" # 로그 저장 경로
MAX_LOG_SIZE=$((10 * 1024 * 1024))        # 로그 최대 크기: 10MB
MAX_LOG_FILES=10                          # 최대 보관 파일 수

# ---- 임계값 (이 값 초과 시 경고 출력) ----
CPU_THRESHOLD=20    # CPU 20% 초과 시 경고
MEM_THRESHOLD=10    # 메모리 10% 초과 시 경고
DISK_THRESHOLD=80   # 디스크 80% 초과 시 경고

# ---- 로그 로테이션 함수 ----
# 로그 파일이 10MB 초과되면 자동으로 순환 (monitor.log.1, .2 ... .10)
rotate_log() {
    [ ! -f "$LOG_FILE" ] && return
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

# ---- 현재 시각 기록 ----
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "====== SYSTEM MONITOR RESULT ======"
echo ""

# =============================================================
# [1] HEALTH CHECK — 프로세스 및 포트 확인
# 비정상 시 exit 1로 즉시 종료 (치명적 오류이므로)
# =============================================================
echo "[HEALTH CHECK]"

# 프로세스 확인
PID=$(pgrep -f "$APP_PROCESS" | head -1)
if [ -z "$PID" ]; then
    # -z: 변수가 비어있으면(프로세스 없으면) FAIL
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

# =============================================================
# [2] 방화벽 상태 점검 — 경고만, 종료 안 함
# =============================================================
echo "[FIREWALL CHECK]"
if systemctl is-active --quiet ufw 2>/dev/null; then
    echo "Firewall (UFW)... [OK] Active"
else
    echo "[WARNING] Firewall (UFW) is not active!"
fi
echo ""

# =============================================================
# [3] 리소스 수집 — CPU / 메모리 / 디스크
# =============================================================
echo "[RESOURCE MONITORING]"

# CPU 사용률 (top 명령으로 수집)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=$(printf "%.1f" "${CPU_USAGE:-0}")

# 메모리 사용률 (free 명령으로 수집)
MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
MEM_USED=$(free  | grep Mem | awk '{print $3}')
if [ "${MEM_TOTAL:-0}" -gt 0 ]; then
    MEM_USAGE=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED / $MEM_TOTAL) * 100}")
else
    MEM_USAGE="0.0"
fi

# 디스크 사용률 (루트 파티션 기준)
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

echo "CPU Usage  : ${CPU_USAGE}%"
echo "MEM Usage  : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USAGE}%"
echo ""

# =============================================================
# [4] 임계값 초과 시 경고 출력 — 종료 안 함
# =============================================================
CPU_INT=$(echo "$CPU_USAGE" | cut -d'.' -f1)
[ "${CPU_INT:-0}"  -gt "$CPU_THRESHOLD"  ] && \
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"

MEM_INT=$(echo "$MEM_USAGE" | cut -d'.' -f1)
[ "${MEM_INT:-0}"  -gt "$MEM_THRESHOLD"  ] && \
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"

[ "${DISK_USAGE:-0}" -gt "$DISK_THRESHOLD" ] && \
    echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"

echo ""
echo "===================================="

# =============================================================
# [5] 로그 기록 — 한 줄씩 누적 저장
# =============================================================
LOG_DIR=$(dirname "$LOG_FILE")
[ ! -d "$LOG_DIR" ] && mkdir -p "$LOG_DIR" 2>/dev/null

rotate_log  # 10MB 초과 시 자동 순환

# >> : 누적 기록 (> 쓰면 이전 로그가 모두 삭제되니 주의!)
echo "[${TIMESTAMP}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%" >> "$LOG_FILE"

echo "[INFO] Log appended: $LOG_FILE"
```

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

```bash
# 파일 소유자 및 권한 설정
# 소유자: agent-dev, 그룹: agent-core
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh

# 750 = 소유자(rwx) + 그룹(r-x) + 기타(---)
# agent-admin은 agent-core 그룹 소속이므로 실행 가능
sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh

# 확인
sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
# 기대: -rwxr-x--- 1 agent-dev agent-core ... monitor.sh

# 테스트 실행 (앱이 실행 중이어야 함)
su - agent-admin -c "/home/agent-admin/agent-app/bin/monitor.sh"

# 로그 확인
cat /var/log/agent-app/monitor.log
```

---

### 9단계 — crontab 자동 실행 등록

**왜 하나요?**
매분 사람이 직접 스크립트를 실행할 수 없습니다. cron이 자동으로 실행해 줍니다.

```
crontab 시간 형식:
* * * * *  명령어
│ │ │ │ └─ 요일 (0=일요일 ~ 6=토요일)
│ │ │ └─── 월 (1-12)
│ │ └───── 일 (1-31)
│ └─────── 시 (0-23)
└───────── 분 (0-59)

* * * * * = 매분 실행
0 2 * * * = 매일 새벽 2시 실행
```

```bash
# agent-admin 계정으로 전환
su - agent-admin

# crontab 편집 (처음 실행 시 편집기 선택 → 1번 nano)
crontab -e

# 맨 아래에 추가:
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
# >> : 실행 출력도 로그에 누적
# 2>&1 : 오류 출력도 함께 저장

# 저장: Ctrl+O → Enter → Ctrl+X

# 등록 확인
crontab -l

# cron 서비스 실행 확인
sudo systemctl status cron
# active (running) 이어야 함
# 아니면: sudo systemctl start cron && sudo systemctl enable cron
```

```bash
# 1~2분 후 로그가 자동으로 쌓이는지 확인
tail -f /var/log/agent-app/monitor.log
# 매분 새 줄이 추가되면 성공! Ctrl+C로 종료
```

---

### 10단계 — 최종 검증 체크리스트

수행 내역서 제출 전 아래 명령어를 **모두 실행하고 스크린샷** 찍으세요.

```bash
# ✅ 1. SSH 설정 확인
grep -E "^Port|^PermitRootLogin" /etc/ssh/sshd_config

# ✅ 2. SSH 포트 리슨 확인
sudo ss -tulnp | grep sshd

# ✅ 3. 방화벽 규칙 확인
sudo ufw status

# ✅ 4. 계정 그룹 소속 확인
id agent-admin && id agent-dev && id agent-test

# ✅ 5. 디렉토리 권한 확인
sudo ls -la /home/agent-admin/agent-app/

# ✅ 6. ACL 확인
getfacl /var/log/agent-app

# ✅ 7. 환경 변수 확인
su - agent-admin -c "echo AGENT_HOME=\$AGENT_HOME"

# ✅ 8. 앱 Boot Sequence 확인 (5단계 모두 [OK])
su - agent-admin -c "/home/agent-admin/agent-app/agent-app-linux-x86"

# ✅ 9. monitor.sh 실행 결과 확인
su - agent-admin -c "/home/agent-admin/agent-app/bin/monitor.sh"

# ✅ 10. 로그 누적 확인
tail -20 /var/log/agent-app/monitor.log

# ✅ 11. crontab 등록 확인
su - agent-admin -c "crontab -l"
```

---

## 5. 과제 완료 후 설명해야 할 내용

과제를 마친 후, 아래 질문들에 스스로 답할 수 있어야 합니다.

### 보안 관련

**Q. SSH 포트를 22에서 20022로 바꾸면 왜 더 안전한가요?**
> 전 세계 해커의 자동화 봇은 기본 포트 22번을 집중적으로 스캔합니다. 포트를 바꾸면 이런 자동화 공격 대부분을 피할 수 있습니다. 포트 변경은 "완벽한 보안"이 아니라 "불필요한 공격 노출을 줄이는" 조치입니다.

**Q. Root 원격 접속을 왜 차단해야 하나요?**
> Root는 서버의 모든 것을 제어할 수 있는 최고 권한 계정입니다. 비밀번호가 탈취되면 서버 전체를 잃습니다. 일반 계정으로 접속 후 필요한 경우만 sudo를 사용하면, 비밀번호가 유출되어도 피해를 최소화할 수 있습니다.

**Q. 방화벽에서 필요한 포트만 허용하는 이유는?**
> 열려있는 포트 = 잠재적인 공격 경로입니다. 20022(SSH)와 15034(앱) 외 모든 포트를 차단하면 공격할 수 있는 경로 자체를 없앱니다.

### 계정/권한 관련

**Q. agent-common과 agent-core 그룹을 왜 분리했나요?**
> upload_files(업로드 공간)는 admin, dev, test 모두 써야 하지만, api_keys(비밀 키)와 로그는 admin, dev만 봐야 합니다. 그룹을 분리하면 "공유해야 할 것"과 "보호해야 할 것"을 명확히 구분할 수 있습니다.

**Q. ACL이 일반 chmod와 어떻게 다른가요?**
> chmod는 "소유자/그룹/나머지" 세 가지만 설정 가능합니다. ACL은 특정 사용자나 그룹에게 개별적으로 권한을 부여할 수 있어 더 세밀한 제어가 가능합니다.

### 운영/자동화 관련

**Q. 환경 변수를 .bashrc에 등록하면 어떤 장점이 있나요?**
> 경로가 변경되면 .bashrc의 변수 하나만 수정하면 됩니다. 스크립트 여러 곳에 경로를 직접 써두면 바꿀 때 모두 찾아서 수정해야 합니다.

**Q. monitor.sh에서 프로세스/포트 FAIL은 exit 1로 종료하고, 방화벽 비활성은 WARNING만 출력하는 이유는?**
> 앱 프로세스가 없거나 포트가 닫히면 서비스가 실제로 다운된 것 → 즉시 알려야 합니다.
> 방화벽 비활성은 위험하지만 앱 자체는 동작 중 → 경고만 남기고 모니터링은 계속합니다.
> "치명적 오류"와 "경고"를 구분하는 것이 좋은 모니터링 설계의 핵심입니다.

**Q. 로그에 `>>` 대신 `>`를 쓰면 어떻게 되나요?**
> `>`는 파일을 덮어씁니다. 매분 실행될 때마다 이전 로그가 모두 삭제되어 로그가 항상 1줄만 남게 됩니다. `>>`는 파일 끝에 이어 쓰므로 누적 기록이 됩니다.

**Q. 로그 로테이션이 왜 필요한가요?**
> 매분 기록되는 로그를 방치하면 디스크가 가득 찹니다. 10MB 제한과 10개 파일 순환으로 최대 100MB만 사용하도록 제한합니다.

**Q. crontab의 `* * * * *`는 무슨 의미인가요?**
> 분/시/일/월/요일이 모두 `*`(와일드카드) = "모든 시간" = **매분 실행**입니다.

---

## 6. 자주 발생하는 문제 해결

| 문제 | 원인 | 해결 |
|---|---|---|
| `Permission denied` on ls | 다른 계정에서 홈 디렉토리 접근 | `sudo ls -la ...` 사용 |
| monitor.sh `Permission denied` | 계정 확인 필요 | `whoami` → agent-admin이어야 함 |
| 로그에 기록 안 됨 | `/var/log/agent-app` 권한 문제 | `ls -la /var/log/agent-app` 확인 |
| cron이 실행 안 됨 | 앱이 꺼져있거나 cron 서비스 중단 | `pgrep -f agent-app`, `systemctl status cron` |
| Boot [3/5] FAIL | 키 파일 내용 불일치 | `cat -A $AGENT_KEY_PATH` 확인 → 공백/줄바꿈 제거 |

---

## 7. 제출 체크리스트

| 항목 | 제출물 |
|---|---|
| 수행 내역서 | 설정/명령어 기록 + 스크린샷 |
| SSH 설정 | Port 20022, PermitRootLogin no 스크린샷 |
| 방화벽 | ufw status 스크린샷 |
| 계정/그룹 | id agent-admin/dev/test 스크린샷 |
| 디렉토리 권한 | ls -la + getfacl 스크린샷 |
| Boot Sequence | 5단계 [OK] + "Agent READY" 스크린샷 |
| monitor.sh | 실행 결과 스크린샷 |
| 로그 누적 | tail monitor.log (3줄 이상) 스크린샷 |
| crontab | crontab -l 스크린샷 |
| 소스코드 | monitor.sh 파일 |
