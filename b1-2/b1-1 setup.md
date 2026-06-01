# B1-1 환경 자동 복구 가이드

> 매주 월요일 포맷 후 `b1-1 setup.sh` 스크립트를 실행하면 B1-1 전체 환경이 자동으로 복구됩니다.

---

## 실행 방법 (포맷 후 순서)

### 1단계 — OrbStack VM 접속

```bash
# macOS 터미널에서
orb shell b1-lab
```

### 2단계 — GitHub에서 스크립트 받기

```bash
# VM 안에서
git clone https://github.com/linksat1/AI-SW-Basic
cd AI-SW-Basic/b1-2
```

### 3단계 — 스크립트 실행

```bash
chmod +x "b1-1 setup.sh"
sudo bash "b1-1 setup.sh"
```

완료까지 약 **2~3분** 소요됩니다.

---

## 스크립트가 수행하는 작업

### STEP 1 — 필수 패키지 설치

| 패키지 | 용도 |
|---|---|
| `acl` | 세밀한 권한 제어(ACL) 도구 |
| `ufw` | 방화벽 도구 |
| `net-tools` | 네트워크 확인 도구 |
| `cron` | 자동 실행 스케줄러 |

---

### STEP 2 — 그룹 및 계정 생성

**생성되는 그룹:**

| 그룹 | 접근 가능 디렉토리 |
|---|---|
| `agent-common` | upload_files (admin, dev, test 모두) |
| `agent-core` | api_keys, 로그 (admin, dev만) |

**생성되는 계정:**

| 계정 | 비밀번호 | 소속 그룹 | 권한 |
|---|---|---|---|
| `agent-admin` | Admin1234 | common, core, sudo | 관리자 |
| `agent-dev` | Dev1234 | common, core | 개발자 |
| `agent-test` | Test1234 | common | 테스터 |

---

### STEP 3 — 디렉토리 구조 생성

```
/home/agent-admin/agent-app/
├── upload_files/    ← agent-common 그룹 공유 (rwx)
├── api_keys/        ← agent-core 그룹 전용 (r-x)
└── bin/             ← 스크립트 보관

/var/log/agent-app/  ← agent-core 그룹 로그 (rwx)
```

---

### STEP 4 — 앱 파일 및 키 파일

**앱 바이너리 자동 탐색 경로 (순서대로 시도):**
```
1. /mac/Users/cspag5955/.../b1-1/실행파일/agent-app-linux-arm64
2. /mac/Users/cspag5955/.../b1-1/실행파일/agent-app-linux-x86
3. /tmp/agent-app-linux-arm64
4. /tmp/agent-app-linux-x86
```

> 위 경로에 파일이 없으면 수동으로 복사해야 합니다:
> ```bash
> cp /tmp/agent-app-linux-x86 /home/agent-admin/agent-app/agent-app
> chmod +x /home/agent-admin/agent-app/agent-app
> ```

**생성되는 키 파일:**

| 파일 | 경로 | 용도 |
|---|---|---|
| `t_secret.key` | api_keys/t_secret.key | B1-1 앱 인증 |
| `secret.key` | api_keys/secret.key | B1-2 앱 인증 |

---

### STEP 5 — 환경변수 (.bashrc 자동 등록)

`agent-admin` 계정으로 로그인하면 아래 변수들이 자동으로 적용됩니다:

```bash
# B1-1 환경변수
AGENT_HOME=/home/agent-admin/agent-app
AGENT_PORT=15034
AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
AGENT_KEY_PATH=$AGENT_HOME/api_keys/t_secret.key
AGENT_LOG_DIR=/var/log/agent-app

# B1-2 추가 환경변수
MEMORY_LIMIT=256          # 메모리 상한선 (MB)
CPU_MAX_OCCUPY=50         # CPU 최대 점유율 (%)
MULTI_THREAD_ENABLE=true  # 멀티스레드 여부
```

---

### STEP 6 — monitor.sh 설치 및 crontab 등록

**monitor.sh 위치 및 권한:**

| 항목 | 값 |
|---|---|
| 경로 | `/home/agent-admin/agent-app/bin/monitor.sh` |
| 소유자 | agent-dev |
| 그룹 | agent-core |
| 권한 | 750 (rwxr-x---) |

**crontab (agent-admin):**
```
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.log 2>&1
```
→ 매분 자동 실행

---

## 복구 완료 후 확인 명령어

```bash
# 계정 그룹 확인
id agent-admin

# 환경변수 확인
su - agent-admin -c "echo AGENT_HOME=\$AGENT_HOME"

# crontab 확인
crontab -u agent-admin -l

# 디렉토리 권한 확인
ls -la /home/agent-admin/agent-app/
```

---

## 스크립트 실행 후 별도 설정 필요 항목

> 아래 두 항목은 포맷 후 직접 설정해야 합니다 (스크립트 미포함).

### SSH 보안 설정

```bash
sudo nano /etc/ssh/sshd_config
# Port 20022
# PermitRootLogin no

sudo systemctl restart sshd
```

### 방화벽(UFW) 설정

```bash
sudo ufw allow 20022/tcp
sudo ufw allow 15034/tcp
sudo ufw enable
sudo ufw status
```

---

## 앱 실행

```bash
su - agent-admin
/home/agent-admin/agent-app/agent-app
```

5단계 모두 **[OK]** 와 **"Agent READY"** 가 출력되면 정상입니다.
