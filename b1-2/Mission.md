# B1-2 미션 교본 — 리눅스 프로세스 및 시스템 리소스 트러블슈팅

> **대상:** 리눅스 입문자 (처음 장애 분석을 해보는 분)
> **환경:** macOS + OrbStack + Ubuntu 22.04
> **학습 시간:** 약 40시간 (실습 포함)

---

## 1. 이 미션은 무엇인가요?

### 한 줄 요약
> "실제 서버에서 발생하는 3가지 장애(메모리 누수, CPU 과점유, 교착상태)를 직접 재현하고, 로그를 증거로 원인을 분석하여 GitHub Issue 형태의 기술 보고서를 작성한다."

### 왜 이 미션이 중요한가요?

실제 서버 운영에서 이런 일이 생깁니다:
- 새벽 2시에 서버가 갑자기 죽음 → "왜 죽었지?" → 로그 없으면 감으로만 추측
- 특정 시간대에 CPU가 100%로 치솟음 → 어떤 프로세스가 범인인지 모름
- 프로세스가 살아있는데 아무것도 안 함 → 죽은 건지 살아있는 건지 모름

이 미션은 이런 장애를 **데이터로 증명하고 리포트로 남기는 능력**을 키웁니다.

### 3가지 장애 유형

| 장애 유형 | 현상 | 원인 |
|---|---|---|
| **Memory Leak (OOM)** | 프로세스가 갑자기 종료됨 | 메모리를 계속 할당만 하고 해제하지 않음 |
| **CPU Spike** | CPU 사용률이 급상승 후 프로세스 종료 | 특정 연산이 CPU를 독점 |
| **Deadlock** | 프로세스가 살아있으나 완전히 멈춤 | 두 스레드가 서로의 자원을 무한 대기 |

### 미션이 끝나면 할 수 있는 것

| 할 수 있는 것 | 왜 중요한가 |
|---|---|
| 메모리 누수 패턴을 로그로 식별 | 장애 원인 추적의 기본 |
| CPU 과점유 프로세스 특정 | 성능 문제 진단 |
| Deadlock 상태를 시스템 도구로 진단 | 무응답 원인 규명 |
| GitHub Issue 형태로 기술 리포트 작성 | 팀과의 기술 커뮤니케이션 |

---

## 2. 환경 설정

### 2-1. B1-1 환경이 전제조건

B1-2는 B1-1에서 만든 환경(계정, 디렉토리, 환경변수)을 그대로 사용합니다.
B1-1을 완료하지 않았다면 먼저 완료하세요.

**B1-1에서 필요한 것:**
```
✅ agent-admin 계정
✅ AGENT_HOME, AGENT_PORT 등 환경변수
✅ /home/agent-admin/agent-app/ 디렉토리 구조
✅ monitor.sh (매분 자동 실행 중)
```

### 2-2. 추가 환경변수 설정

B1-2 앱(`agent-leak-app`)은 아래 3가지 환경변수가 추가로 필요합니다.

```bash
# agent-admin 계정으로 전환
su - agent-admin

# .bashrc에 추가 환경변수 등록
cat >> /home/agent-admin/.bashrc << 'EOF'

# ===== B1-2 추가 환경변수 =====
export MEMORY_LIMIT=256          # 메모리 상한선 (MB, 범위: 50~512)
export CPU_MAX_OCCUPY=50         # CPU 최대 점유율 (%, 범위: 10~100)
export MULTI_THREAD_ENABLE=true  # 멀티스레드 사용 여부 (true/false)
EOF

# 즉시 적용
source /home/agent-admin/.bashrc

# 확인
echo "MEMORY_LIMIT      : $MEMORY_LIMIT"
echo "CPU_MAX_OCCUPY    : $CPU_MAX_OCCUPY"
echo "MULTI_THREAD_ENABLE: $MULTI_THREAD_ENABLE"
```

### 2-3. 앱 파일 준비

```bash
# macOS 터미널(새 창)에서 실행 — orb shell 밖에서!
# Apple Silicon (M1/M2) Mac:
orb push b1-lab \
  /Users/cspag5955/OrbStack/AI-SW-ubuntu24/home/cspag5955/AI-SW-Basic/b1-1/실행파일/agent-app-linux-arm64 \
  /tmp/agent-leak-app

# Intel Mac:
orb push b1-lab \
  /Users/cspag5955/OrbStack/AI-SW-ubuntu24/home/cspag5955/AI-SW-Basic/b1-1/실행파일/agent-app-linux-x86 \
  /tmp/agent-leak-app
```

```bash
# VM 안(agent-admin 계정)에서:
cp /tmp/agent-leak-app /home/agent-admin/agent-app/
chmod +x /home/agent-admin/agent-app/agent-leak-app
# chmod +x: 실행 권한 부여
```

### 2-4. secret.key 파일 확인

B1-2는 기존 `t_secret.key`가 아닌 `secret.key`를 사용합니다.

```bash
# secret.key 생성 (내용은 정확히 agent_api_key_test)
echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key
chmod 600 /home/agent-admin/agent-app/api_keys/secret.key

# 내용 확인
cat /home/agent-admin/agent-app/api_keys/secret.key
# 기대: agent_api_key_test
```

### 2-5. 앱 정상 실행 확인

```bash
# agent-admin 계정에서 실행
cd /home/agent-admin/agent-app
./agent-leak-app
```

아래처럼 **5단계 모두 [OK]** 이고 **"Agent READY"** 가 나와야 합니다:
```
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
[2/5] Verifying Environment Variables     [OK]
[3/5] Checking Required Files             [OK]
[4/5] Checking Port Availability          [OK]
[5/5] Verifying Log Permission            [OK]
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
```

---

## 3. 전체 과제 흐름

```
[준비]
  B1-1 환경 확인 → 추가 환경변수 설정 → agent-leak-app 배치
       ↓
[케이스 1: Memory Leak / OOM]
  앱 실행 → monitor.sh로 메모리 상승 관측
       ↓
  메모리 임계치 도달 → 앱 자동 종료 (SELF-TERMINATED)
       ↓
  로그 분석 → 원인 규명 → MEMORY_LIMIT 조정 → Before/After 비교
       ↓
  GitHub Issue 리포트 작성 (OOM)
       ↓
[케이스 2: CPU Spike]
  앱 실행 → CPU 사용률 급상승 관측 (top/ps/monitor.sh)
       ↓
  Watchdog 정책으로 앱 종료 (SIGTERM)
       ↓
  로그 분석 → 원인 규명 → CPU_MAX_OCCUPY 조정 → Before/After 비교
       ↓
  GitHub Issue 리포트 작성 (CPU)
       ↓
[케이스 3: Deadlock]
  앱 실행 (MULTI_THREAD_ENABLE=true) → PID는 있으나 로그 멈춤
       ↓
  ps/top으로 무응답 상태 확인 → 마지막 로그에서 BLOCKED 확인
       ↓
  MULTI_THREAD_ENABLE=false로 변경 → 정상 동작 확인
       ↓
  GitHub Issue 리포트 작성 (Deadlock)
       ↓
[최종 제출]
  3개 GitHub Issue 리포트 → PDF 또는 GitHub Repository 링크 제출
```

---

## 4. 단계별 따라하기

---

### 케이스 1: Memory Leak (메모리 누수) 분석

#### 개념 먼저 이해하기

**메모리 누수란?**
프로그램이 메모리를 빌려 쓰고 반납하지 않는 것입니다.
마치 도서관에서 책을 빌리고 반납을 안 하면 결국 빌릴 책이 없어지는 것처럼,
메모리가 가득 차면 시스템이 불안정해집니다.

```
정상 동작:   메모리 할당 → 사용 → 해제 → 할당 → ...  (일정하게 유지)
메모리 누수:  메모리 할당 → 사용 → [해제 안 함] → 또 할당 → ...  (계속 증가)
```

#### 4-1-1. 앱 실행 및 모니터링 시작

**터미널 A** — 앱 실행:
```bash
# agent-admin 계정에서
su - agent-admin
cd /home/agent-admin/agent-app

# MEMORY_LIMIT=256 (기본값)으로 실행
./agent-leak-app
# 앱이 실행되고 로그가 출력되기 시작함
# 이 터미널은 그대로 둠 (앱 실행 유지)
```

**터미널 B** (새로 열기) — 메모리 모니터링:
```bash
# VM에 접속
orb shell b1-lab

# 실시간으로 메모리 변화 관찰 (매 3초마다 갱신)
watch -n 3 'ps -eo pid,comm,%mem,rss --sort=-%mem | head -10'
# %mem: 메모리 사용률
# rss: 실제 사용 중인 물리 메모리 (KB)
```

**터미널 C** (새로 열기) — monitor.log 실시간 확인:
```bash
orb shell b1-lab

# 로그가 쌓이는 것을 실시간으로 확인
tail -f /var/log/agent-app/monitor.log
# 매분 새 줄이 추가되며 MEM 수치가 올라가는 것을 관찰
```

#### 4-1-2. 장애 발생 확인

약 10분 후 터미널 A에서 아래 메시지가 출력되며 앱이 종료됩니다:
```
[CRITICAL] [MemoryGuard] Memory limit exceeded (256MB >= 256MB)
[CRITICAL] [MemoryGuard] Self-terminating process XXXX to prevent system instability.
>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<
```

**이 시점에서 해야 할 것:**
```bash
# monitor.log에서 메모리 상승 패턴 캡처
cat /var/log/agent-app/monitor.log
# MEM 수치가 서서히 증가하는 것을 확인 → 스크린샷 저장

# 앱 실행 로그 확인 (앱이 출력한 로그)
# → 터미널 A의 출력 내용 스크린샷 저장
```

#### 4-1-3. 조치 — MEMORY_LIMIT 조정

```bash
# agent-admin 계정에서 .bashrc 수정
nano /home/agent-admin/.bashrc

# MEMORY_LIMIT 값 변경:
# export MEMORY_LIMIT=256  →  export MEMORY_LIMIT=512
# (더 큰 메모리 한계치로 조정하여 더 오래 생존하는지 확인)

# 저장 후 적용
source /home/agent-admin/.bashrc
echo "MEMORY_LIMIT: $MEMORY_LIMIT"
# 기대: 512

# 앱 재실행 (변경 후)
./agent-leak-app
# 이전보다 훨씬 오래(30분 이상) 생존하는지 확인
```

#### 4-1-4. 리포트 작성 (GitHub Issue 형식)

아래 템플릿으로 마크다운 파일을 작성하세요:

```markdown
# [Bug] 메모리 누수로 인한 MemoryGuard 보호 정책 강제 종료

## 1. Description (현상 설명)
- 어떤 현상이 발생했는가?
  → agent-leak-app 실행 약 10분 후 "SELF-TERMINATED" 메시지와 함께 프로세스 강제 종료
- 언제, 어떤 조건에서?
  → MEMORY_LIMIT=256 설정 상태, 정상 실행 중

## 2. Evidence & Logs (증거 자료)
[monitor.log 데이터 — 메모리 상승 구간 발췌]
[2026-XX-XX 14:00:00] ... MEM:5.1% ...
[2026-XX-XX 14:03:00] ... MEM:35.4% ...
[2026-XX-XX 14:09:00] ... MEM:89.5% ...
[2026-XX-XX 14:10:00] ... MEM:96.8% ...

[앱 실행 로그 — 종료 직전 핵심 로그]
[CRITICAL] [MemoryGuard] Memory limit exceeded (256MB >= 256MB)
[CRITICAL] [MemoryGuard] Self-terminating process XXXX ...
>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<

## 3. Root Cause Analysis (원인 분석)
- 앱 내부에서 메모리를 할당 후 해제하지 않는 메모리 누수(Memory Leak) 발생
- 물리 메모리 사용량이 MEMORY_LIMIT(256MB)에 도달하자 MemoryGuard 정책이 동작
- SIGKILL로 프로세스 강제 종료 → 시스템 전체 불안정 방지

## 4. Workaround & Verification (조치 및 검증)
- 조치: MEMORY_LIMIT을 256MB → 512MB로 상향 조정
- Before: MEMORY_LIMIT=256 → 약 10분 후 종료
- After:  MEMORY_LIMIT=512 → 30분 이상 생존 확인
- 근본 해결: 소스코드에서 불필요한 데이터를 주기적으로 해제하는 리팩토링 필요
```

---

### 케이스 2: CPU Spike (CPU 과점유) 분석

#### 개념 먼저 이해하기

**CPU 과점유란?**
CPU는 여러 프로세스가 나눠 쓰는 공용 자원입니다.
하나의 프로세스가 CPU를 독점하면 다른 프로세스들이 처리되지 못해 시스템 전체가 느려집니다.
이를 방지하기 위해 앱 내부에 Watchdog(감시자)이 설정된 임계치 초과 시 프로세스를 종료합니다.

#### 4-2-1. 앱 실행 및 CPU 모니터링

```bash
# 환경변수 확인 (CPU_MAX_OCCUPY 기본값)
echo $CPU_MAX_OCCUPY   # 50

# 앱 실행
su - agent-admin
cd /home/agent-admin/agent-app
./agent-leak-app
```

**새 터미널에서 CPU 모니터링:**
```bash
# 방법 1: top으로 실시간 확인
top
# P키: CPU 사용률 기준 정렬
# q: 종료

# 방법 2: 특정 프로세스만 추적
watch -n 1 'ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -10'
# --sort=-%cpu: CPU 내림차순 정렬

# 방법 3: monitor.log로 CPU 추이 확인
tail -f /var/log/agent-app/monitor.log
```

#### 4-2-2. 장애 발생 확인

CPU 사용률이 `CPU_MAX_OCCUPY`를 초과하면 앱이 종료됩니다:
```
[WARNING] [Watchdog] CPU usage spike detected: 75.3% > 50%
[CRITICAL] [Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)
>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<
```

**증거 수집:**
```bash
# CPU 급상승 구간 스크린샷 저장
# top 또는 watch 출력 결과 캡처

# monitor.log에서 CPU 상승 구간 발췌
grep "CPU" /var/log/agent-app/monitor.log | tail -20
```

#### 4-2-3. 조치 — CPU_MAX_OCCUPY 조정

```bash
# .bashrc에서 CPU_MAX_OCCUPY 값 수정
nano /home/agent-admin/.bashrc
# export CPU_MAX_OCCUPY=50  →  export CPU_MAX_OCCUPY=90
# (더 높은 임계치로 설정하여 Watchdog이 늦게 작동하게 함)

source /home/agent-admin/.bashrc
echo "CPU_MAX_OCCUPY: $CPU_MAX_OCCUPY"
# 기대: 90

# 앱 재실행 — CPU가 90%를 넘지 않으면 종료되지 않음
./agent-leak-app
```

#### 4-2-4. 리포트 작성

```markdown
# [Bug] CPU 과점유에 의한 Watchdog 보호 조치 프로세스 종료

## 1. Description (현상 설명)
- agent-leak-app 실행 후 CPU 사용률이 급격히 상승
- "[SYSTEM] WATCHDOG: INITIATING EMERGENCY ABORT" 메시지와 함께 종료
- CPU_MAX_OCCUPY=50 설정 상태에서 재현

## 2. Evidence & Logs (증거 자료)
[monitor.log — CPU 급상승 구간]
[2026-XX-XX] CPU:2.1% ...
[2026-XX-XX] CPU:35.6% ...
[2026-XX-XX] CPU:72.4% ...

[앱 실행 로그 — Watchdog 작동 로그]
[WARNING] [Watchdog] CPU usage spike detected: 75.3% > 50%
[CRITICAL] [Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)
>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<

[top/ps 출력 — 프로세스별 CPU 점유율]
(스크린샷 첨부)

## 3. Root Cause Analysis (원인 분석)
- 앱 내부의 특정 연산이 CPU를 집중적으로 사용하는 로직 존재
- CPU 사용률이 CPU_MAX_OCCUPY(50%)를 초과하자 Watchdog 정책이 동작
- SIGTERM으로 프로세스 종료 → 시스템 전체 부하 방지

## 4. Workaround & Verification (조치 및 검증)
- 조치: CPU_MAX_OCCUPY를 50% → 90%로 상향 조정
- Before: CPU_MAX_OCCUPY=50 → CPU 50% 초과 시 즉시 종료
- After:  CPU_MAX_OCCUPY=90 → CPU 90% 미만 구간에서 정상 동작 유지
- 근본 해결: CPU를 독점하는 연산을 분산 처리하거나 sleep을 삽입하는 코드 개선 필요
```

---

### 케이스 3: Deadlock (교착상태) 분석

#### 개념 먼저 이해하기

**교착상태(Deadlock)란?**
두 스레드가 서로의 자원을 기다리며 영원히 진행하지 못하는 상태입니다.

예시 — 식사하는 철학자 문제:
```
철학자 A: 왼쪽 젓가락 들고 → 오른쪽 젓가락 기다리는 중
철학자 B: 오른쪽 젓가락 들고 → 왼쪽 젓가락 기다리는 중
→ 둘 다 상대방의 젓가락을 기다리며 영원히 대기 (아무도 밥을 못 먹음)
```

**교착상태 4대 조건 (모두 충족될 때 발생):**

| 조건 | 설명 |
|---|---|
| 상호 배제 | 자원은 한 번에 하나의 스레드만 사용 가능 |
| 점유 대기 | 자원을 가진 채로 다른 자원을 기다림 |
| 비선점 | 다른 스레드의 자원을 강제로 빼앗을 수 없음 |
| 순환 대기 | A→B→C→A처럼 순환하며 서로 기다림 |

**교착상태 식별 방법:**
```
정상 프로세스: PID 있음 + CPU/MEM 변화 있음 + 로그 출력 중
Deadlock 상태: PID 있음 + CPU/MEM 변화 없음 + 로그 완전히 멈춤
```

#### 4-3-1. Deadlock 재현

```bash
# MULTI_THREAD_ENABLE=true (기본값, 멀티스레드 활성화)
echo $MULTI_THREAD_ENABLE   # true

# 앱 실행
su - agent-admin
cd /home/agent-admin/agent-app
./agent-leak-app
```

**새 터미널에서 상태 모니터링:**
```bash
# 스레드 단위로 CPU/MEM 변화 확인
watch -n 2 'ps -L -p $(pgrep -f agent-leak-app) -o pid,tid,pcpu,pmem,stat'
# -L: 스레드 목록
# stat: 상태 (S=대기, R=실행, D=IO대기)

# 또는 top으로 스레드 단위 확인
top -H -p $(pgrep -f agent-leak-app)
# -H: 스레드 단위로 표시
# -p: 특정 PID만 표시
```

#### 4-3-2. Deadlock 확인 방법

잠시 후 앱이 종료되지 않고 로그만 멈추는 것을 확인합니다:

```bash
# 1. PID가 살아있는지 확인
ps -ef | grep agent-leak-app
# PID가 존재해야 함

# 2. CPU/MEM 변화 없음 확인
# top 또는 watch 결과에서 CPU, MEM이 고정됨을 확인

# 3. 마지막 로그 확인 (로그가 멈춘 지점)
tail -20 /var/log/agent-app/monitor.log
# 또는 앱 출력 로그에서
# "WAITING...", "BLOCKED", "DEADLOCK" 관련 메시지 확인

# 4. 프로세스 상태(stat) 확인
ps -eo pid,stat,comm | grep agent-leak
# stat D: Uninterruptible sleep (자원 대기 중)
```

**마지막 로그 예시:**
```
[Thread-A] Acquired Lock-1, WAITING for Lock-2...
[Thread-B] Acquired Lock-2, WAITING for Lock-1...
(이후 로그 없음 → 두 스레드가 서로를 영원히 기다리는 중)
```

#### 4-3-3. 조치 — MULTI_THREAD_ENABLE 조정

```bash
# 프로세스 강제 종료
kill $(pgrep -f agent-leak-app)
# kill: 프로세스 정상 종료 신호(SIGTERM)
# kill -9: 강제 종료 (안 죽으면 사용)

# .bashrc에서 멀티스레드 비활성화
nano /home/agent-admin/.bashrc
# export MULTI_THREAD_ENABLE=true  →  export MULTI_THREAD_ENABLE=false

source /home/agent-admin/.bashrc
echo "MULTI_THREAD_ENABLE: $MULTI_THREAD_ENABLE"
# 기대: false

# 재실행 — 데드락 없이 정상 동작해야 함
./agent-leak-app
```

#### 4-3-4. 리포트 작성

```markdown
# [Bug] 멀티스레드 환경에서 교착상태(Deadlock) 발생으로 프로세스 무응답

## 1. Description (현상 설명)
- agent-leak-app 실행 후 프로세스가 종료되지 않고 PID 유지
- CPU/메모리 변화 없이 로그 출력도 완전히 멈춘 무응답 상태 지속
- MULTI_THREAD_ENABLE=true 상태에서 재현

## 2. Evidence & Logs (증거 자료)
[PID 존재 확인]
ps -ef | grep agent-leak-app
→ (PID 출력됨 — 프로세스 살아있음)

[스레드별 CPU/MEM 변화 없음]
top -H -p XXXX
→ 모든 스레드 CPU 0%, 상태 고정

[마지막 로그 발췌 — 교착 진입 지점]
[Thread-A] Acquired Lock-1, WAITING for Lock-2...
[Thread-B] Acquired Lock-2, WAITING for Lock-1...
(이후 로그 없음)

## 3. Root Cause Analysis (원인 분석)
- Thread-A: Lock-1 보유 → Lock-2 대기
- Thread-B: Lock-2 보유 → Lock-1 대기
- 교착상태 4대 조건 중 순환 대기(Circular Wait) 발생
- 두 스레드가 서로의 자원을 영원히 기다려 진행 불가

## 4. Workaround & Verification (조치 및 검증)
- 조치: MULTI_THREAD_ENABLE=false로 변경 (싱글스레드 모드)
- Before: true  → 멀티스레드 → 교착상태 발생 → 무응답
- After:  false → 싱글스레드 → 자원 경쟁 없음 → 정상 동작
- 근본 해결: 락 획득 순서를 통일하거나 타임아웃을 설정하는 코드 개선 필요
```

---

## 5. 유용한 명령어 모음

```bash
# 프로세스 목록 확인
ps -ef | grep agent-leak-app          # 프로세스 존재 여부
ps -eo pid,comm,%cpu,%mem --sort=-%cpu # CPU 기준 정렬

# 스레드 단위 분석
top -H -p $(pgrep -f agent-leak-app)  # 스레드별 실시간 모니터링
ps -L -p $(pgrep -f agent-leak-app)   # 스레드 목록

# 메모리 분석
free -h                               # 전체 메모리 현황
cat /proc/$(pgrep -f agent-leak-app)/status | grep VmRSS  # 특정 프로세스 물리 메모리

# 로그 분석
tail -f /var/log/agent-app/monitor.log         # 실시간 로그 확인
grep "MEM" /var/log/agent-app/monitor.log      # 메모리 수치만 추출
grep "CPU" /var/log/agent-app/monitor.log      # CPU 수치만 추출

# 프로세스 종료
kill $(pgrep -f agent-leak-app)       # 정상 종료 (SIGTERM)
kill -9 $(pgrep -f agent-leak-app)    # 강제 종료 (SIGKILL, 안 죽을 때)
```

---

## 6. 과제 완료 후 설명해야 할 내용

### 메모리 관련

**Q. 메모리 누수(Memory Leak)가 시스템에 미치는 영향은?**
> 메모리는 OS 전체가 공유하는 자원입니다. 한 프로세스가 메모리를 계속 독점하면 다른 프로세스들이 메모리를 할당받지 못해 전체 시스템이 느려지거나 OOM(Out of Memory) 상태가 됩니다. 심하면 OS가 프로세스를 강제 종료(OOM Killer)합니다.

**Q. MEMORY_LIMIT을 높이는 것이 근본 해결책인가요?**
> 아닙니다. 임시방편입니다. 메모리 누수가 있으면 한계치만 높일 뿐 결국 더 많은 메모리를 써서 또 죽습니다. 근본 해결은 코드에서 사용 후 메모리를 해제(del, free)하는 것입니다.

### CPU 관련

**Q. CPU 과점유가 시스템 전체에 어떤 영향을 미치나요?**
> CPU는 시분할(time-sharing)로 여러 프로세스에 나눠집니다. 하나가 CPU를 독점하면 다른 프로세스들의 응답이 지연됩니다. 웹 서버라면 모든 요청이 느려지고, 결국 타임아웃이 발생합니다.

**Q. Watchdog이 SIGTERM을 보내는 이유는?**
> SIGTERM은 "정상적으로 종료하라"는 신호입니다. 프로세스가 이 신호를 받으면 마무리 작업(파일 닫기, 로그 저장 등) 후 종료됩니다. 강제 종료(SIGKILL)와 달리 데이터 손실 없이 안전하게 종료됩니다.

### Deadlock 관련

**Q. Deadlock의 4대 조건이란?**
> 상호 배제(자원은 하나만), 점유 대기(갖고 기다림), 비선점(강제 빼앗기 불가), 순환 대기(A→B→A). 이 4가지가 동시에 충족될 때 교착상태가 발생합니다. 4가지 중 하나만 없애면 교착상태를 막을 수 있습니다.

**Q. Deadlock 프로세스를 어떻게 식별하나요?**
> PID는 있는데 CPU/MEM 변화가 없고 로그도 멈췄다면 교착상태를 의심합니다. `top -H`로 스레드 상태가 모두 대기(S, D)인지 확인하고, 마지막 로그에서 WAITING/BLOCKED 패턴을 찾습니다.

**Q. MULTI_THREAD_ENABLE=false가 근본 해결책인가요?**
> 아닙니다. 멀티스레드를 끄면 성능 이점도 사라집니다. 근본 해결은 락 획득 순서를 통일하거나(Thread-A와 B 모두 Lock-1 먼저 획득 후 Lock-2), 타임아웃을 설정하여 일정 시간 후 대기를 포기하도록 코드를 개선하는 것입니다.

### 리포팅 관련

**Q. GitHub Issue 형태로 리포트를 작성하는 이유는?**
> 장애 원인을 혼자만 알고 끝내면 같은 장애가 반복됩니다. 팀원이 읽을 수 있는 구조화된 문서로 남기면 (1) 재현 방법을 공유하고, (2) 조치 결과를 검증하고, (3) 나중에 유사 장애 시 참고할 수 있습니다.

---

## 7. 자주 발생하는 문제 해결

| 문제 | 원인 | 해결 |
|---|---|---|
| Boot [2/5] FAIL | 추가 환경변수 미설정 | `source ~/.bashrc` 후 재실행 |
| Boot [3/5] FAIL | secret.key 내용 불일치 | `cat $AGENT_HOME/api_keys/secret.key` 확인 |
| monitor.log에 로그 없음 | 앱 프로세스가 없어서 monitor.sh가 exit 1로 종료 | 앱 먼저 실행 후 monitor.sh 실행 |
| Deadlock 앱이 안 죽음 | 정상 — Deadlock은 종료 없이 무응답 상태 | `kill $(pgrep -f agent-leak-app)`으로 수동 종료 |
| kill이 안 됨 | D 상태(Uninterruptible sleep) | `kill -9 PID`로 강제 종료 |

---

## 8. 제출 체크리스트

### 리포트 3건 (각각 GitHub Issue 또는 마크다운)

| 항목 | OOM | CPU | Deadlock |
|---|---|---|---|
| 현상 설명 | ✅ | ✅ | ✅ |
| monitor.log 발췌 | ✅ | ✅ | ✅ |
| 앱 실행 로그 발췌 | ✅ | ✅ | ✅ |
| ps/top 출력 캡처 | ✅ | ✅ | ✅ |
| 근본 원인 분석 | ✅ | ✅ | ✅ |
| Before & After 비교 | ✅ | ✅ | ✅ |

### 필수 스크린샷 목록

| 번호 | 캡처 내용 |
|---|---|
| 1 | monitor.log — OOM 발생 전 메모리 상승 구간 |
| 2 | 앱 로그 — SELF-TERMINATED 메시지 |
| 3 | monitor.log — CPU 급상승 구간 |
| 4 | 앱 로그 — WATCHDOG SIGTERM 메시지 |
| 5 | ps -ef — Deadlock 상태에서 PID 존재 확인 |
| 6 | top -H — 스레드별 CPU 변화 없음 |
| 7 | 앱 로그 — WAITING/BLOCKED 마지막 로그 |
| 8 | 각 케이스 MEMORY_LIMIT / CPU_MAX_OCCUPY / MULTI_THREAD_ENABLE 변경 후 정상 동작 |
