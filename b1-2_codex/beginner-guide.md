# B1-2 초보자용 따라하기 교본

> 미션: `agent-leak-app`에서 발생하는 3가지 장애(OOM/Memory Leak, CPU Spike, Deadlock)를 재현하고, 로그와 명령어 출력으로 원인을 분석한 뒤 GitHub Issue 형식의 리포트 3개를 작성합니다.

---

## 0. 이 교본의 사용법

이 문서는 **명령어를 그대로 따라 치는 방식**으로 구성되어 있습니다.

- `#`으로 시작하는 줄은 설명 주석입니다. 터미널에 입력하지 않아도 됩니다.
- 명령어 아래의 `기대 결과`는 정상적으로 되었는지 확인하는 기준입니다.
- 이 교본은 **원본 실행 파일 `agent-leak-app`을 기준으로 실습**합니다.

---

## 1. 미션 전체 그림

| 케이스 | 관찰할 현상 | 조정할 환경변수 | 최종 리포트 |
|---|---|---|---|
| 1. Memory Leak / OOM | 메모리 사용량이 계속 증가하거나 보호 정책으로 종료됨 | `MEMORY_LIMIT` | `reports/oom.md` |
| 2. CPU Spike | 특정 프로세스 CPU 사용률이 급상승하고 Watchdog/SIGTERM 종료됨 | `CPU_MAX_OCCUPY` | `reports/cpu-spike.md` |
| 3. Deadlock | PID는 살아있지만 CPU/메모리/로그 변화가 멈춤 | `MULTI_THREAD_ENABLE` | `reports/deadlock.md` |
| 선택 보너스. Scheduling | 로그 실행 순서로 스케줄링 방식을 추론 | 앱 실행 로그 | `reports/scheduling-analysis.md` |

핵심은 “느낌상 그런 것 같다”가 아니라 **로그, `ps`, `top`, `monitor.sh` 결과로 증명**하는 것입니다.

---

## 2. 준비물 확인

### 2-1. 현재 위치 확인

```bash
# pwd는 현재 내가 어느 폴더에 있는지 보여줍니다.
pwd
```

기대 결과:

```text
/Users/cspag5955/Documents
```

### 2-2. 제공 파일 확인

```bash
# ls는 폴더 안의 파일 목록을 보여줍니다.
# b1-2 폴더 안에 앱과 미션 자료가 있는지 확인합니다.
ls -la AI-SW-Basic/b1-2
```

확인할 파일:

- `agent-leak-app-arm64`: Apple Silicon Mac용 리눅스 실행 파일
- `agent-leak-app-x86`: Intel/AMD x86 리눅스 실행 파일
- `b1-2-mission_교제발췌`: 미션 요구사항 원문

---

## 3. 실습 원칙: 원본 앱 기준

이 교본에서는 아래 원칙을 사용합니다.

- 실행 파일은 `agent-leak-app-arm64` 또는 `agent-leak-app-x86`만 사용합니다.
- 관제 증거는 `monitor.sh`, `ps`, `top`, `/proc/<PID>/status`로 수집합니다.
- 기대한 `SELF-TERMINATED`, `WATCHDOG`, `Deadlock` 로그가 나오지 않으면 **원본 앱에서 재현되지 않았다는 사실 자체를 증거로 리포트**합니다.

중요한 판단:

> 과제의 목적은 “정답 로그를 억지로 만드는 것”이 아니라, 원본 실행 파일을 운영 환경에서 관찰하고 그 결과를 기술적으로 설명하는 것입니다. 원본 앱이 미션 설명과 다르게 동작한다면, 그 차이를 객관적 증거로 남기는 것도 트러블슈팅입니다.

---

## 4. Linux 원본 앱 실행 준비

아래 명령어는 **B1-1에서 만든 OrbStack Ubuntu `b1-lab` 환경**을 그대로 사용한다고 가정합니다.

B1-1과 동일하게 유지할 기준:

| 항목 | B1-1/B1-2 공통값 |
|---|---|
| 실행 계정 | `agent-admin` |
| 앱 홈 | `/home/agent-admin/agent-app` |
| 업로드 디렉터리 | `/home/agent-admin/agent-app/upload_files` |
| 키 디렉터리 | `/home/agent-admin/agent-app/api_keys` |
| 로그 디렉터리 | `/var/log/agent-app` |
| 앱 포트 | `15034` |

주의할 점:

- B1-1 앱은 `t_secret.key`를 사용했습니다.
- B1-2 앱은 `secret.key` 파일이 필요합니다.
- B1-2 미션 요구사항에서 `AGENT_KEY_PATH`는 **키 파일 하나가 아니라 `$AGENT_HOME/api_keys` 디렉터리**로 맞추는 것이 안전합니다.

### 4-1. B1-1 환경 확인

```bash
# Ubuntu VM 안에서 실행합니다.
id agent-admin
ls -ld /home/agent-admin/agent-app
ls -ld /home/agent-admin/agent-app/upload_files
ls -ld /home/agent-admin/agent-app/api_keys
ls -ld /var/log/agent-app
```

기대 결과:

- `agent-admin` 계정이 존재합니다.
- `/home/agent-admin/agent-app` 디렉터리가 존재합니다.
- `/var/log/agent-app`에 `agent-admin` 또는 `agent-core` 그룹이 쓸 수 있습니다.

만약 위 구조가 없다면 먼저 기존 `b1-2/b1-1 setup.md`의 자동 복구 절차를 실행합니다.

```bash
cd ~/AI-SW-Basic/b1-2
chmod +x "b1-1 setup.sh"
sudo bash "b1-1 setup.sh"
```

### 4-2. B1-2용 secret.key 만들기

```bash
# B1-2 앱이 요구하는 키 파일입니다.
# 내용은 반드시 agent_api_key_test여야 합니다.
sudo -u agent-admin bash -c 'echo "agent_api_key_test" > /home/agent-admin/agent-app/api_keys/secret.key'

# 키 파일 권한을 제한합니다.
sudo chmod 600 /home/agent-admin/agent-app/api_keys/secret.key
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys/secret.key

# 내용 확인
sudo -u agent-admin cat /home/agent-admin/agent-app/api_keys/secret.key
```

기대 결과:

```text
agent_api_key_test
```

### 4-3. B1-2 실행 파일 배치

macOS에 있는 파일을 Ubuntu로 복사한 뒤, Ubuntu 안에서 이름을 `agent-leak-app`로 맞춥니다. 미션 원문에서 사용하는 앱 이름이 `agent-leak-app`이므로, 모니터링 스크립트도 이 이름을 기준으로 찾습니다.

macOS 터미널에서 Ubuntu VM으로 복사하는 예시:

```bash
# Apple Silicon Mac이면 arm64 파일을 복사합니다.
orb push b1-lab /Users/cspag5955/Documents/AI-SW-Basic/b1-2/agent-leak-app-arm64 /tmp/agent-leak-app

# Intel Mac 또는 x86_64 Ubuntu 환경이면 x86 파일을 복사합니다.
orb push b1-lab /Users/cspag5955/Documents/AI-SW-Basic/b1-2/agent-leak-app-x86 /tmp/agent-leak-app
```

```bash
# 여기부터는 Ubuntu VM 안에서 실행합니다.
sudo cp /tmp/agent-leak-app /home/agent-admin/agent-app/agent-leak-app
sudo chmod +x /home/agent-admin/agent-app/agent-leak-app
sudo chown agent-admin:agent-admin /home/agent-admin/agent-app/agent-leak-app
```

파일이 실행 가능한지 확인합니다.

```bash
ls -l /home/agent-admin/agent-app/agent-leak-app
```

기대 결과:

```text
-rwxr-xr-x ... /home/agent-admin/agent-app/agent-leak-app
```

`x`가 보이면 실행 권한이 있다는 뜻입니다.

---

## 5. 환경변수 설정

환경변수는 앱이 실행될 때 읽는 설정값입니다.

```bash
# B1-1에서 만든 운영 계정으로 전환합니다.
su - agent-admin

# 실습 폴더로 이동합니다.
cd /home/agent-admin/agent-app

# B1-1과 같은 기준 경로를 사용합니다.
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_LOG_DIR=/var/log/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys

# B1-2에서 추가로 사용하는 환경변수입니다.
export MEMORY_LIMIT=256
export CPU_MAX_OCCUPY=50
export MULTI_THREAD_ENABLE=true
```

설정 확인:

```bash
echo "$AGENT_HOME"
echo "$AGENT_LOG_DIR"
echo "$AGENT_PORT"
echo "$AGENT_UPLOAD_DIR"
echo "$AGENT_KEY_PATH"
echo "$MEMORY_LIMIT"
echo "$CPU_MAX_OCCUPY"
echo "$MULTI_THREAD_ENABLE"
```

---

## 6. 보조 스크립트 복사

이 폴더의 `scripts/monitor.sh`, `scripts/run_helpers.sh`를 B1-1의 앱 홈으로 복사합니다.

```bash
# Ubuntu 안에서 실행합니다.
sudo cp /path/to/b1-2_codex/scripts/monitor.sh /home/agent-admin/agent-app/monitor.sh
sudo cp /path/to/b1-2_codex/scripts/run_helpers.sh /home/agent-admin/agent-app/run_helpers.sh

# agent-admin이 실행할 수 있게 소유자와 실행 권한을 맞춥니다.
sudo chown agent-admin:agent-admin /home/agent-admin/agent-app/monitor.sh /home/agent-admin/agent-app/run_helpers.sh
sudo chmod +x /home/agent-admin/agent-app/monitor.sh /home/agent-admin/agent-app/run_helpers.sh
```

경로가 헷갈리면 `pwd`와 `ls`로 현재 위치를 먼저 확인하세요.

---

## 7. 앱 부팅 확인

```bash
su - agent-admin
cd /home/agent-admin/agent-app
./agent-leak-app
```

기대 결과:

```text
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
[2/5] Verifying Environment Variables     [OK]
[3/5] Checking Required Files             [OK]
[4/5] Checking Port Availability          [OK]
[5/5] Verifying Log Permission            [OK]
All Boot Checks Passed!
Agent READY
```

중지하려면 `Ctrl + C`를 누릅니다.

---

## 8. Case 1: Memory Leak / OOM

### 8-1. Before 실행

터미널 A:

```bash
su - agent-admin
cd /home/agent-admin/agent-app

# 메모리 한계를 낮게 두어 메모리 증가/종료 현상을 관찰합니다.
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_LOG_DIR=/var/log/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export MEMORY_LIMIT=50
export CPU_MAX_OCCUPY=100
export MULTI_THREAD_ENABLE=false

# 앱 로그를 evidence에 저장하면서 실행합니다.
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_oom_before_app.log
```

터미널 B:

```bash
su - agent-admin
cd /home/agent-admin/agent-app

# monitor.sh가 2초마다 PID, CPU, MEM, 포트 상태를 기록합니다.
MONITOR_LOG=/var/log/agent-app/evidence_oom_before_monitor.log ./monitor.sh
```

터미널 C:

```bash
# ps는 현재 실행 중인 프로세스의 자원 사용량을 보여줍니다.
# rss는 실제 메모리 사용량을 KB 단위로 보여줍니다.
ps -eo pid,ppid,user,%cpu,%mem,rss,stat,cmd --sort=-rss | head -10
```

찾을 증거:

- `Memory limit exceeded`
- `Self-terminating process`
- `SELF-TERMINATED`
- `rss` 또는 `%mem` 증가
- 위 종료 로그가 없다면 `rss`가 한계값을 넘었는데도 종료되지 않는지 확인

### 8-2. After 실행

Before가 끝났으면 앱과 모니터를 중지하고 `MEMORY_LIMIT`을 높여 다시 실행합니다.

```bash
pkill -f agent-leak-app
pkill -f monitor.sh

export MEMORY_LIMIT=512
export CPU_MAX_OCCUPY=100
export MULTI_THREAD_ENABLE=false

MONITOR_LOG=/var/log/agent-app/evidence_oom_after_monitor.log ./monitor.sh &
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_oom_after_app.log
```

비교할 것:

- Before보다 오래 살아있는가?
- 종료 로그가 달라졌는가?
- 메모리 사용량의 피크가 달라졌는가?
- 둘 다 종료되지 않는다면 `MEMORY_LIMIT`이 실제 자원 사용량 판정에 반영되지 않는다고 쓸 수 있는가?

---

## 9. Case 2: CPU Spike

### 9-1. Before 실행

```bash
pkill -f agent-leak-app
pkill -f monitor.sh

cd /home/agent-admin/agent-app
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_LOG_DIR=/var/log/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys

# 메모리 때문에 먼저 종료되지 않도록 넉넉히 둡니다.
export MEMORY_LIMIT=512

# CPU 임계치를 높게 또는 낮게 바꿔가며 Watchdog 동작을 관찰합니다.
export CPU_MAX_OCCUPY=10
export MULTI_THREAD_ENABLE=false

MONITOR_LOG=/var/log/agent-app/evidence_cpu_before_monitor.log ./monitor.sh &
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_cpu_before_app.log
```

다른 터미널에서:

```bash
# top은 실시간 자원 사용량을 보여줍니다.
# -p 뒤에는 agent-leak-app의 PID를 넣습니다.
PID=$(pgrep -x agent-leak-app | tail -n 1)
top -p "$PID"
```

또는:

```bash
ps -p "$(pgrep -x agent-leak-app | tail -n 1)" -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
```

찾을 증거:

- `CPU Threshold Violated`
- `WATCHDOG`
- `SIGTERM`
- 특정 PID의 `%CPU` 급상승
- Watchdog 로그가 없다면 `%CPU`가 임계치보다 높은데도 종료되지 않는지 확인

### 9-2. After 실행

```bash
pkill -f agent-leak-app
pkill -f monitor.sh

export MEMORY_LIMIT=512
export CPU_MAX_OCCUPY=50
export MULTI_THREAD_ENABLE=false

MONITOR_LOG=/var/log/agent-app/evidence_cpu_after_monitor.log ./monitor.sh &
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_cpu_after_app.log
```

비교할 것:

- CPU 임계치 변경 후 종료 시점이 달라졌는가?
- Watchdog이 발동했는가?
- cooldown 또는 정상 지속 실행 로그가 있는가?
- 둘 다 종료되지 않는다면 `CPU_MAX_OCCUPY`가 실제 Watchdog 발동에 영향을 주지 않는다고 쓸 수 있는가?

---

## 10. Case 3: Deadlock

### 10-1. Before 실행

```bash
pkill -f agent-leak-app
pkill -f monitor.sh

cd /home/agent-admin/agent-app
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_LOG_DIR=/var/log/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export MEMORY_LIMIT=512
export CPU_MAX_OCCUPY=100

# 데드락을 재현하려면 멀티스레드를 켭니다.
export MULTI_THREAD_ENABLE=true

MONITOR_LOG=/var/log/agent-app/evidence_deadlock_before_monitor.log ./monitor.sh &
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_deadlock_before_app.log
```

다른 터미널에서:

```bash
# PID가 살아있는지 확인합니다.
ps -ef | grep agent-leak-app

# 스레드 목록을 확인합니다.
# -L 옵션은 프로세스 안의 스레드까지 보여줍니다.
PID=$(pgrep -x agent-leak-app | tail -n 1)
ps -L -p "$PID" -o pid,tid,stat,%cpu,%mem,comm

# 스레드별 CPU 사용량을 실시간으로 봅니다.
top -H -p "$PID"
```

찾을 증거:

- PID가 계속 존재함
- CPU/MEM 변화가 거의 없음
- 앱 로그가 `WAITING`, `BLOCKED` 근처에서 멈춤
- 스레드는 있는데 진행이 없음

### 10-2. After 실행

```bash
pkill -f agent-leak-app
pkill -f monitor.sh

export MEMORY_LIMIT=512
export CPU_MAX_OCCUPY=100

# 데드락 회피 비교를 위해 멀티스레드를 끕니다.
export MULTI_THREAD_ENABLE=false

MONITOR_LOG=/var/log/agent-app/evidence_deadlock_after_monitor.log ./monitor.sh &
./agent-leak-app 2>&1 | tee /var/log/agent-app/evidence_deadlock_after_app.log
```

비교할 것:

- `MULTI_THREAD_ENABLE=true`일 때 멈췄는가?
- `false`일 때 같은 지점에서 멈추지 않는가?
- 마지막 로그가 달라졌는가?
- `true`에서도 스레드가 1개이고 로그가 계속 진행된다면 Deadlock 재현 로직이 활성화되지 않는다고 쓸 수 있는가?

---

## 11. 원본 앱에서 기대 결과가 안 나올 때

원본 `agent-leak-app`을 사용하면 미션 설명처럼 `SELF-TERMINATED`, `WATCHDOG`, `WAITING/BLOCKED`가 반드시 나오는 것은 아닐 수 있습니다. 이때 아래처럼 “안 나온다”는 사실을 증거로 남깁니다.

### 11-1. 부모/자식 프로세스 모두 확인

```bash
ps -ef | grep agent-leak-app
pgrep -x agent-leak-app
ps -C agent-leak-app -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
```

확인할 것:

- PID가 1개인지 2개 이상인지
- 부모 프로세스와 자식 프로세스 중 실제 CPU/MEM을 쓰는 쪽이 누구인지
- `monitor.sh`가 실제 부하 프로세스를 기록하고 있는지

### 11-2. 실제 메모리 사용량 확인

```bash
PID=$(pgrep -x agent-leak-app | tail -n 1)
grep -E "Name|State|VmRSS|VmSize|Threads" /proc/$PID/status
```

리포트에 쓸 수 있는 해석:

- `VmRSS`가 `MEMORY_LIMIT`보다 큰데도 종료되지 않으면 MemoryGuard가 실제 RSS 기준으로 발동하지 않았다고 추론할 수 있습니다.
- 앱 로그의 `Total: 275 MB` 같은 내부 카운터와 `/proc/<PID>/status`의 `VmRSS`가 다르면, 로그 값과 OS 실측값이 다르다고 기록합니다.

### 11-3. 실제 CPU 사용량 확인

```bash
PID=$(pgrep -x agent-leak-app | tail -n 1)
top -bn1 -p "$PID"
ps -p "$PID" -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
```

리포트에 쓸 수 있는 해석:

- `%CPU`가 `CPU_MAX_OCCUPY`보다 큰데도 `WATCHDOG` 또는 `SIGTERM` 로그가 없다면 Watchdog이 실제 CPU 사용률 기준으로 발동하지 않았다고 추론할 수 있습니다.

### 11-4. Deadlock 확인

```bash
PID=$(pgrep -x agent-leak-app | tail -n 1)
ps -L -p "$PID" -o pid,tid,stat,%cpu,%mem,comm
grep Threads /proc/$PID/status
grep -iE "thread|deadlock|waiting|blocked|lock" /var/log/agent-app/evidence_deadlock_before_app.log
```

리포트에 쓸 수 있는 해석:

- `MULTI_THREAD_ENABLE=true`인데 `Threads: 1`이면 멀티스레드가 실제로 생성되지 않은 것입니다.
- `WAITING`, `BLOCKED`, `Lock` 로그가 없고 PEAK/BOTTOM 로그가 계속 반복되면 Deadlock이 재현되지 않은 것입니다.

### 11-5. 결론 작성 방향

원본 앱 결과가 미션 설명과 다르면 리포트 제목을 이렇게 잡을 수 있습니다.

```text
[Bug] 원본 agent-leak-app에서 MEMORY_LIMIT 초과 후 MemoryGuard가 발동하지 않음
[Bug] 원본 agent-leak-app에서 CPU_MAX_OCCUPY 초과 후 Watchdog이 발동하지 않음
[Bug] 원본 agent-leak-app에서 MULTI_THREAD_ENABLE=true에도 Deadlock이 재현되지 않음
```

이 경우에도 리포트 구조는 동일합니다.

1. 어떤 조건으로 실행했는지 적습니다.
2. 기대한 로그가 없었다는 grep 결과를 붙입니다.
3. `ps`, `top`, `/proc` 결과로 실제 자원 상태를 보여줍니다.
4. 환경변수 변경 전후가 실제 동작에 영향을 주지 않았음을 비교합니다.

---

## 12. 증거 파일 정리

실습이 끝나면 `/var/log/agent-app`에서 만든 증거 파일을 이 폴더의 `evidence/logs/`로 모읍니다.

권장 파일 이름:

```text
evidence/logs/oom_before_app.log
evidence/logs/oom_before_monitor.log
evidence/logs/oom_after_app.log
evidence/logs/oom_after_monitor.log
evidence/logs/cpu_before_app.log
evidence/logs/cpu_before_monitor.log
evidence/logs/cpu_after_app.log
evidence/logs/cpu_after_monitor.log
evidence/logs/deadlock_before_app.log
evidence/logs/deadlock_before_monitor.log
evidence/logs/deadlock_after_app.log
evidence/logs/deadlock_after_monitor.log
```

추가로 저장하면 좋은 파일:

```text
evidence/logs/cpu_before_ps.log
evidence/logs/cpu_before_top.log
evidence/logs/deadlock_before_ps.log
evidence/logs/deadlock_before_threads.log
evidence/logs/deadlock_before_topH.log
```

---

## 13. 리포트 작성 방법

`templates/github-issue-template.md`를 복사해서 3개의 리포트를 만듭니다.

```bash
cp templates/github-issue-template.md reports/oom.md
cp templates/github-issue-template.md reports/cpu-spike.md
cp templates/github-issue-template.md reports/deadlock.md
```

각 리포트에는 반드시 아래 4개 항목을 채웁니다.

1. `Description`: 어떤 현상이 언제, 어떤 조건에서 발생했는가?
2. `Evidence & Logs`: 어떤 로그/명령어 출력이 증거인가?
3. `Root Cause Analysis`: 그 증거로 어떤 원인을 추론했는가?
4. `Workaround & Verification`: 환경변수 조정 전후 결과가 어떻게 달라졌는가?

---

## 14. 선택 보너스: 스케줄링 알고리즘 추론

보너스 과제는 필수 제출물은 아니지만, 로그를 더 깊게 읽는 연습에 좋습니다.

### 14-1. 수집할 로그

정상 실행 또는 CPU/Deadlock 실습 중 앱 로그에서 아래와 같은 정보를 찾습니다.

- 스레드 이름: `Thread-A`, `Thread-B`, `Worker` 등
- 작업 시작/재개/완료 로그
- 타임스탬프 간격
- 한 작업이 끝나기 전에 다른 작업이 끼어드는지 여부

### 14-2. 판단 기준

| 알고리즘 | 로그에서 보이는 특징 |
|---|---|
| FCFS | 먼저 시작한 작업이 끝난 뒤 다음 작업이 시작됨 |
| Round-Robin | 여러 작업이 짧게 번갈아 실행됨 |
| Priority | 특정 작업이 반복적으로 먼저 실행되거나 더 자주 실행됨 |

### 14-3. 템플릿 복사

```bash
cp templates/scheduling-analysis-template.md reports/scheduling-analysis.md
```

작성할 때는 “정답 맞히기”보다 **왜 그렇게 추론했는지 로그 근거를 제시하는 것**이 중요합니다.

---

## 15. 초보자용 명령어 해설

| 명령어 | 뜻 |
|---|---|
| `pwd` | 현재 위치 출력 |
| `cd /home/agent-admin/agent-app` | B1-1에서 만든 앱 홈 폴더로 이동 |
| `ls -la` | 숨김 파일까지 자세히 목록 출력 |
| `export A=B` | 현재 터미널 세션에 환경변수 설정 |
| `echo "$A"` | 환경변수 값 출력 |
| `chmod +x file` | 파일에 실행 권한 부여 |
| `chown user:user file` | 파일 소유자 변경 |
| `ps -ef` | 전체 프로세스 목록 출력 |
| `ps -L -p PID` | 특정 프로세스의 스레드 목록 출력 |
| `top -p PID` | 특정 프로세스 자원 사용량 실시간 확인 |
| `top -H -p PID` | 특정 프로세스의 스레드별 사용량 확인 |
| `pgrep -x name` | 이름이 정확히 일치하는 프로세스 PID 검색 |
| `pkill -f name` | 이름이 포함된 프로세스 종료 |
| `tee file.log` | 화면에 출력하면서 동시에 파일로 저장 |
| `grep PATTERN file` | 파일에서 원하는 단어가 있는 줄만 찾기 |
| `/proc/<PID>/status` | 리눅스가 제공하는 특정 프로세스의 실제 상태 파일 |

---

## 16. 제출 전 체크리스트

- [ ] OOM 리포트에 메모리 상승 증거가 있다.
- [ ] OOM 리포트에 `MEMORY_LIMIT` 변경 전후 비교가 있다.
- [ ] CPU 리포트에 CPU 급상승 증거가 있다.
- [ ] CPU 리포트에 `CPU_MAX_OCCUPY` 변경 전후 비교가 있다.
- [ ] Deadlock 리포트에 PID 존재, CPU/MEM 정체, 마지막 로그 증거가 있다.
- [ ] Deadlock 리포트에 `MULTI_THREAD_ENABLE=true/false` 비교가 있다.
- [ ] 각 리포트가 GitHub Issue 형식의 4개 섹션을 모두 포함한다.
- [ ] 증거 로그 파일 이름과 리포트에서 참조한 파일 이름이 일치한다.
- [ ] 원본 `agent-leak-app` 로그와 리눅스 명령어 출력 결과를 사용했다.
- [ ] 선택 보너스를 한다면 스케줄링 추론 리포트에 로그 타임스탬프와 실행 순서 근거가 있다.
