# PPT 설명 보완

## 1. OOM 로그 위치

### 질문

아래 내용이 어느 파일에 있는지 확인해.

```text
17:18:00  Current Heap: 25MB
17:18:03  Current Heap: 50MB
Memory limit exceeded (50MB >= 50MB)
Self-terminating process 3114
```

### 답변

해당 내용은 주로 아래 파일에서 확인할 수 있다.

- `b1-2_codex/evidence/logs/oom_before_app.log`
- `b1-2_codex/reports/oom.md`
- `b1-2_codex/reports/evaluation-prep.md`

PPT 생성 스크립트에는 축약된 형태로 들어 있다.

- `b1-2_codex/scripts/make_evaluation_ppt.py`

## 2. 이중 관찰 의미

### 질문

이중 관찰, 앱 내부 Heap 카운터와 OS RSS를 함께 비교해 이중 확인은 무슨 뜻?

### 답변

이중 관찰은 같은 메모리 증가 현상을 두 가지 기준으로 동시에 확인했다는 뜻이다.

- 앱 내부 Heap 카운터: 프로그램이 스스로 기록한 메모리 사용량 로그
- OS RSS: 운영체제가 밖에서 본 실제 프로세스 메모리 사용량

예를 들어 앱 로그에서는 다음처럼 확인된다.

```text
Current Heap: 25MB
Current Heap: 50MB
```

그리고 OS 관측값에서는 RSS가 증가한다.

보고서용 문장:

> 앱 내부 Heap 로그와 OS RSS 값을 함께 비교하여 메모리 증가 현상을 교차 검증했다.

## 3. RSS 증가 확인 위치

### 질문

RSS도 증가 확인은?

### 답변

RSS 증가는 `b1-2_codex/evidence/logs/oom_before_monitor.log`에서 확인한다.

핵심 줄은 다음과 같다.

```text
17:18:00  PID 3114 ... RSS 18628
17:18:02  PID 3114 ... RSS 44232
```

즉 OS가 본 실제 메모리 사용량이 `18628KB`에서 `44232KB`로 증가했다.

`ps` 출력 컬럼 순서가 `%CPU %MEM RSS STAT CMD`이므로, `18628`, `44232`가 RSS 값이다. 단위는 KB이다.

## 4. CPU cooldown 로그 위치

### 질문

아래 내용은 어디에서 확인하지?

```text
CpuWorker Started. Maximum CPU Limit: 10%
Current Load: 5.00%
Peak reached (10.00%). Starting cooldown...
Cooldown complete (5.00%). Resuming...
```

### 답변

원본 증거 파일은 다음이다.

- `b1-2_codex/evidence/logs/cpu_before_app.log`

해당 줄들:

```text
CpuWorker Started. Maximum CPU Limit: 10%
Current Load: 5.00%
Peak reached (10.00%). Starting cooldown...
Cooldown complete (5.00%). Resuming load increase...
```

보고서에는 다음 파일에 정리되어 있다.

- `b1-2_codex/reports/cpu-spike.md`
- `b1-2_codex/reports/evaluation-prep.md`

## 5. CPU, top, thread 명령어 의미

### 질문

```text
ps -C agent-leak-app  |  top -bn1 -p PID  |  ps -L -p PID  (스레드 확인 도구)
```

무슨 뜻?

### 답변

이것은 프로세스와 스레드 상태를 확인하는 명령어 묶음이다. 특히 Deadlock 의심 상황에서 프로세스가 살아 있는지, CPU/메모리는 어떤지, 스레드는 몇 개이고 멈춰 있는지 확인할 때 사용한다.

`ps -C agent-leak-app`

> `agent-leak-app`이라는 이름의 프로세스가 실행 중인지 확인한다.

`top -bn1 -p PID`

> 특정 PID 하나만 골라서 CPU/메모리 상태를 한 번 출력한다.

예:

```bash
top -bn1 -p 3114
```

`ps -L -p PID`

> 특정 PID 안의 스레드 목록을 확인한다.

예:

```bash
ps -L -p 3114
```

주의할 점은 `|` 기호이다. 여기서는 실제 파이프처럼 연결해서 실행한다는 뜻보다는 확인 도구들을 나열한 것에 가깝다. 실제 명령은 각각 따로 실행하는 것이 맞다.

## 6. Deadlock 경고와 Load 로그 위치

### 질문

아래 내용은 어디에 있지?

```text
SYSTEM WARNING: POTENTIAL DEADLOCK
Current Load: 5.00%
Current Load: 10.27%
Current Load: 21.62%
```

### 답변

원본 증거는 다음 파일에 있다.

- `b1-2_codex/evidence/logs/deadlock_before_app.log`

해당 내용:

```text
SYSTEM WARNING: POTENTIAL DEADLOCK IN CONCURRENT MODE.
Current Load: 5.00%
Current Load: 10.27%
Current Load: 21.62%
```

보고서에는 다음 파일에도 정리되어 있다.

- `b1-2_codex/reports/deadlock.md`
- `b1-2_codex/reports/evaluation-prep.md`

## 7. WAITING/BLOCKED/lock 로그 없음 의미

### 질문

`WAITING/BLOCKED/lock 로그 없음`은 무슨 말?

### 답변

이 말은 진짜 데드락이라고 볼 만한 직접 증거가 없었다는 뜻이다.

데드락은 보통 여러 스레드가 서로 자원을 잡고 놓지 않아서, 서로 기다리기만 하고 더 이상 진행하지 못하는 상태이다.

데드락을 확인하려면 보통 이런 증거가 필요하다.

- `WAITING`: 스레드가 어떤 조건이나 자원을 기다리는 상태
- `BLOCKED`: 스레드가 락을 얻지 못해서 막힌 상태
- `lock` 관련 로그: lock 획득 대기, mutex 대기, deadlock detected 같은 메시지

이번 로그에서는 경고 문구는 있었지만 이후에도 `Current Load`가 계속 증가했다. 즉 프로그램이 멈춘 게 아니라 계속 동작한 것이다.

또한 `Threads: 1`로 확인됐기 때문에, 여러 스레드가 서로 기다리는 전형적인 데드락 상황이라고 보기 어렵다.

보고서용 문장:

> Deadlock 경고는 출력됐지만, 스레드가 대기 또는 차단 상태에 빠졌다는 `WAITING`, `BLOCKED`, `lock` 관련 로그가 없고 CpuWorker 로그가 계속 진행되어 실제 데드락으로 판단하지 않았다.

## 8. PID 존재 확인 의미

### 질문

진단 도구와 판단 흐름에서 `1. PID 존재 확인`은 무슨 뜻?

### 답변

PID 존재 확인은 문제의 프로그램 프로세스가 아직 살아 있는지 먼저 확인한다는 뜻이다.

PID는 Process ID, 즉 실행 중인 프로세스 번호이다. 예를 들어 `agent-leak-app`이 실행 중이면 OS가 `3455` 같은 번호를 붙인다.

먼저 확인하는 이유:

- PID가 없으면 프로세스가 이미 종료된 상태이므로 OOM 종료, crash, self-terminate 쪽을 의심한다.
- PID가 있으면 프로세스는 살아 있으므로 CPU/RSS 변화, 스레드 상태, 로그 진행 여부를 추가로 본다.
- PID는 있는데 로그가 멈추고 스레드가 `WAITING` 또는 `BLOCKED`이면 Deadlock 가능성이 커진다.

확인 명령 예:

```bash
pgrep agent-leak-app
ps -C agent-leak-app
```

보고서용 문장:

> 먼저 `pgrep` 또는 `ps -C agent-leak-app`으로 PID가 존재하는지 확인한다. PID가 없으면 프로세스 종료 원인을 분석하고, PID가 있으면 CPU/RSS 변화와 스레드 상태를 추가로 확인한다.

## 9. 진단 도구 목록 의미

### 질문

```text
monitor.sh:  pgrep -x agent-leak-app
             ps -p PID -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
CPU:         ps -C agent-leak-app  |  top -bn1 -p PID
Thread:      ps -L -p PID  |  top -H -bn1 -p PID  |
```

무슨 뜻?

### 답변

이것은 장애 진단할 때 어떤 명령어로 무엇을 확인했는지 정리한 표이다. `|`는 실제 파이프라기보다 "또는 / 같이 쓰는 도구"라는 뜻으로 보는 것이 맞다.

`monitor.sh`

```bash
pgrep -x agent-leak-app
ps -p PID -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
```

뜻:

> `agent-leak-app` 프로세스가 살아 있는지 PID를 찾고, 그 PID의 CPU, 메모리, RSS, 상태를 확인한다.

`CPU`

```bash
ps -C agent-leak-app
top -bn1 -p PID
```

뜻:

> 해당 프로세스의 CPU 사용률을 확인한다.

`Thread`

```bash
ps -L -p PID
top -H -bn1 -p PID
```

뜻:

> 특정 프로세스 안의 스레드 목록과 스레드별 CPU 상태를 확인한다.

보고서용 문장:

> `monitor.sh`에서는 `pgrep`으로 PID 존재 여부를 확인하고, `ps`로 CPU/MEM/RSS/상태를 수집했다. CPU 상태는 `ps -C`와 `top`으로 확인했으며, Deadlock 판단을 위해 `ps -L`과 `top -H`로 스레드 수와 스레드별 상태를 확인했다.

## 10. 확인 결과 로그 위치

### 질문

확인한 결과에 대한 로그는?

### 답변

확인 결과 로그는 케이스별로 `*_monitor.log`와 `*_ps.log`에 있다.

Deadlock 기준:

- PID 존재 / CPU / RSS 확인: `b1-2_codex/evidence/logs/deadlock_before_monitor.log`
- `ps`, `/proc`, `top`, `ps -L`, `top -H` 결과: `b1-2_codex/evidence/logs/deadlock_before_ps.log`

핵심 판단 근거:

```text
Threads: 1
PID     TID STAT %CPU %MEM COMMAND
3455    3455 SN   0.5  0.1 agent-leak-app
```

CPU 케이스:

- `b1-2_codex/evidence/logs/cpu_before_monitor.log`
- `b1-2_codex/evidence/logs/cpu_before_ps.log`

OOM 케이스:

- `b1-2_codex/evidence/logs/oom_before_monitor.log`
- `b1-2_codex/evidence/logs/oom_before_ps.log`

## 11. monitor.sh 위치

### 질문

`monitor.sh`를 찾아줘.

### 답변

실습 로그들과 직접 연결되는 파일은 다음이다.

- `b1-2_codex/scripts/monitor.sh`

비슷한 참고/이전 파일도 있다.

- `b1-2/bangahee-reference/monitor.sh`
- `b1-1/scripts/monitor.sh`

`b1-2_codex/scripts/monitor.sh` 안에서 `pgrep -x agent-leak-app`으로 PID를 찾고, `ps -p "$PID" -o ... rss ...`로 CPU/MEM/RSS 상태를 로그에 남긴다.

## 12. CPU 도구 선택 이유

### 질문

```text
Q. CPU 도구 선택 이유?
A. ps는 스냅샷, top은 실시간/순간 부하, ps -L은 스레드 확인
```

위 내용을 설명해줘.

### 답변

이 문장은 CPU 문제를 볼 때 왜 `ps`, `top`, `ps -L`을 각각 썼는지 설명하는 내용이다.

`ps`는 스냅샷이다.

> 특정 시점에 프로세스가 어떤 상태인지 한 번 찍어서 보여준다.

예:

```bash
ps -p PID -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
```

그래서 보고서에 "이 시점에 이 프로세스는 CPU 0.5%, RSS 18720KB였다"처럼 증거로 남기기 좋다.

`top`은 실시간 또는 순간 부하 확인이다.

> 시스템이 지금 얼마나 바쁜지, 특정 프로세스가 CPU를 얼마나 쓰고 있는지 확인한다.

예:

```bash
top -bn1 -p PID
```

여기서 `-bn1`은 실시간 화면을 계속 보는 대신 한 번만 출력해서 로그에 남기겠다는 뜻이다. 그래서 `ps`보다 CPU 부하 상황을 운영 관점에서 보기 좋다.

`ps -L`은 스레드 확인이다.

> 하나의 프로세스 안에 스레드가 몇 개 있는지, 각 스레드 상태가 어떤지 확인한다.

예:

```bash
ps -L -p PID
```

Deadlock은 보통 여러 스레드가 서로 기다리는 문제라서, 스레드 수와 상태 확인이 중요하다. 이번 경우에는 `Threads: 1`이라서 실제 데드락이라고 보기 어렵다는 판단 근거가 됐다.

보고서용 문장:

> `ps`는 특정 시점의 프로세스 상태를 스냅샷으로 남기기 위해 사용했고, `top`은 순간 CPU 부하와 시스템 관점의 사용률을 확인하기 위해 사용했다. `ps -L`은 Deadlock 여부 판단에 필요한 스레드 수와 스레드별 상태를 확인하기 위해 사용했다.
