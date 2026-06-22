# B1-2 평가 대비 설명 자료

이 문서는 `b1-2/b1-2-mission_교제발췌`의 요구사항과 `b1-2/b1-2질문`의 평가 질문을 기준으로, 오늘 원본 `agent-leak-app-x86` 실행 결과를 설명하기 위한 발표/질의응답 자료입니다.

## 1. 한 줄 요약

오늘 실습은 OrbStack Ubuntu `b1-lab`에서 원본 `agent-leak-app-x86`를 실행하고, `monitor.sh`, 앱 로그, `ps`, `top`, `/proc/<PID>/status`, `ps -L` 결과를 근거로 OOM, CPU Spike, Deadlock 3개 케이스를 GitHub Issue 형식으로 정리한 작업입니다.

중요한 점은 CPU와 Deadlock은 교재 예시처럼 완전히 재현되지 않았다는 것입니다. 그래서 리포트에는 억지로 정답 로그를 만들지 않고, 원본 앱에서 실제 관찰된 결과와 교재 기대 결과의 차이를 증거 기반으로 기록했습니다.

## 2. 제출물 위치

| 구분 | 파일 |
|---|---|
| OOM 리포트 | `b1-2_codex/reports/oom.md` |
| CPU Spike 리포트 | `b1-2_codex/reports/cpu-spike.md` |
| Deadlock 리포트 | `b1-2_codex/reports/deadlock.md` |
| 증거 로그 | `b1-2_codex/evidence/logs/` |
| 실행 교본 | `b1-2_codex/beginner-guide.md` |

## 3. 교재 요구사항과 오늘 결과 매핑

| 교재 요구사항 | 오늘 확인 결과 | 평가 때 설명할 포인트 |
|---|---|---|
| OOM: 메모리 상승 수치 관찰 | `Current Heap: 25MB → 50MB`, monitor RSS `18628 → 44232KB` 관찰 | 앱 내부 Heap 로그와 OS RSS 관측값을 함께 봤다. |
| OOM: MemoryGuard 종료 로그 | `Memory limit exceeded`, `Self-terminating process` 확인 | `MEMORY_LIMIT=50`에서 보호 정책이 즉시 발동했다. |
| OOM: `MEMORY_LIMIT` Before/After | 50MB에서는 종료, 512MB에서는 관찰 시간 내 종료 없음 | 환경변수 조정이 생존 시간에 영향을 줬다. |
| CPU: CPU 상승 구간 식별 | 앱 로그에서 `Current Load`와 `Peak reached` 확인, `ps`/`top` 스냅샷 수집 | 원본 앱에서는 Watchdog 종료 대신 cooldown 동작이 관찰됐다. |
| CPU: Watchdog/SIGTERM 종료 로그 | 미관찰 | 미션 기대와 원본 앱 실제 동작이 달랐음을 증거로 보고했다. |
| CPU: `CPU_MAX_OCCUPY` Before/After | 10%에서는 cooldown 반복, 50%에서는 24.78%까지 상승 | 임계치가 앱 내부 부하 제어에 반영됐다. |
| Deadlock: PID 존재, CPU/MEM 정체 | PID 존재와 낮은 CPU/MEM은 확인 | 하지만 `Threads: 1`이라 실제 데드락으로 판단하지 않았다. |
| Deadlock: WAITING/BLOCKED 로그 | 미관찰 | 경고 문구만 있고 lock 대기 증거가 없었다. |
| Deadlock: `MULTI_THREAD_ENABLE` Before/After | `true`에서는 경고 출력, `false`에서는 경고 없음 | 환경변수가 경고에는 반영되지만 실제 데드락은 재현되지 않았다. |
| Format: GitHub Issue 구조 | 3개 리포트 모두 현상, 증거, 원인, 조치 구조 | 교재 템플릿을 유지했다. |

## 4. 실행 환경 설명

발표 때 이렇게 설명하면 됩니다.

```text
실행 환경은 OrbStack Ubuntu b1-lab입니다.
원본 바이너리는 오늘 다운로드한 agent-app-leak.zip에서 압축해제한 agent-leak-app-x86와 동일한 파일인지 SHA-256으로 확인했습니다.
실행 계정은 agent-admin이고, 앱 홈은 /home/agent-admin/agent-app입니다.
AGENT_KEY_PATH는 secret.key 파일이 들어 있는 /home/agent-admin/agent-app/api_keys 디렉터리로 설정했습니다.
```

핵심 환경변수:

```text
AGENT_HOME=/home/agent-admin/agent-app
AGENT_LOG_DIR=/var/log/agent-app
AGENT_PORT=15034
AGENT_UPLOAD_DIR=/home/agent-admin/agent-app/upload_files
AGENT_KEY_PATH=/home/agent-admin/agent-app/api_keys
```

원본 파일 동일성 확인:

```text
VM /home/agent-admin/agent-app/agent-leak-app
로컬 b1-2/실행파일/agent-leak-app-x86
zip 내부 agent-leak-app-x86

SHA-256:
7e0a19cfa80ece6b547a5008273661f0d4d71e526e96b51e0d0f341dd1bb3e40
```

## 5. Case 1: OOM 설명 스크립트

### 발표용 설명

```text
OOM 케이스에서는 MEMORY_LIMIT을 50MB로 낮춰서 MemoryGuard 발동을 빠르게 관찰했습니다.
앱 로그에서 MemoryWorker가 Heap을 25MB, 50MB로 증가시키는 것을 확인했고,
50MB에 도달하자 MemoryGuard가 memory limit exceeded 로그를 남기고 자기 종료했습니다.
monitor.sh 로그에서도 실행 중이던 agent-leak-app PID가 다음 스냅샷에서 사라졌고 포트도 닫힌 것을 확인했습니다.
After에서는 MEMORY_LIMIT을 512MB로 올렸고, 같은 관찰 시간 안에서는 종료 로그가 나오지 않았습니다.
따라서 MEMORY_LIMIT 조정이 프로세스 생존 시간에 영향을 준다고 판단했습니다.
```

### 핵심 증거

앱 로그:

```text
2026-06-22 17:18:00,605 [INFO] [MemoryWorker] Current Heap: 25MB
2026-06-22 17:18:03,656 [INFO] [MemoryWorker] Current Heap: 50MB
2026-06-22 17:18:03,657 [CRITICAL] [MemoryGuard] Memory limit exceeded (50MB >= 50MB) / (Recommend Over 256MB)
2026-06-22 17:18:03,657 [CRITICAL] [MemoryGuard] Self-terminating process 3114 to prevent system instability.
```

모니터 로그:

```text
[Mon Jun 22 17:18:02 KST 2026]
PID 3114 RSS 44232KB

[Mon Jun 22 17:18:04 KST 2026]
PROCESS: FAIL - agent-leak-app is NOT running
PORT: WARN - 15034 is not listening
```

### OS 개념 설명

메모리 누수는 프로그램이 힙에 할당한 데이터를 더 이상 쓰지 않는데도 해제하지 않아 사용량이 계속 증가하는 현상입니다. 이 앱에서는 내부 Heap 카운터가 `MEMORY_LIMIT`에 도달하면 MemoryGuard가 시스템 전체 불안정을 막기 위해 프로세스를 스스로 종료합니다. OS 관점에서는 RSS가 실제 물리 메모리 사용량을 보여주고, 앱 로그는 앱 내부에서 계산한 Heap 증가 상태를 보여줍니다.

## 6. Case 2: CPU Spike 설명 스크립트

### 발표용 설명

```text
CPU 케이스에서는 CPU_MAX_OCCUPY를 10으로 낮춘 before와 50으로 높인 after를 비교했습니다.
before에서는 CpuWorker가 10%에 도달하면 Peak reached 로그를 남기고 cooldown으로 들어갔습니다.
after에서는 24.78%까지 부하가 증가했지만 50% 임계치에는 도달하지 않아 cooldown이 관찰되지 않았습니다.
교재 예시는 Watchdog/SIGTERM 종료를 기대하지만, 오늘 원본 앱 실행에서는 WATCHDOG, SIGTERM, CPU Threshold Violated 로그가 나오지 않았습니다.
그래서 저는 CPU Spike 자체와 환경변수 영향은 확인했고, Watchdog 종료는 원본 앱에서 재현되지 않았다고 보고했습니다.
```

### 핵심 증거

Before:

```text
2026-06-22 17:18:49,035 [INFO] [CpuWorker] Started. Maximum CPU Limit: 10%
2026-06-22 17:18:49,035 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:18:51,146 [INFO] [CpuWorker] Peak reached (10.00%). Starting cooldown...
2026-06-22 17:18:57,376 [INFO] [CpuWorker] Cooldown complete (5.00%). Resuming load increase...
```

After:

```text
2026-06-22 17:19:09,079 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:19:15,307 [INFO] [CpuWorker] Current Load: 12.71%
2026-06-22 17:19:18,421 [INFO] [CpuWorker] Current Load: 22.66%
2026-06-22 17:19:21,539 [INFO] [CpuWorker] Current Load: 24.78%
```

시스템 명령:

```text
ps -C agent-leak-app -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
top -bn1 -p <PID>
ps -L -p <PID> -o pid,tid,stat,%cpu,%mem,comm
```

### OS 개념 설명

CPU 과점유는 특정 프로세스가 CPU 시간을 과도하게 사용해 같은 서버의 다른 프로세스 응답성을 떨어뜨리는 상황입니다. `ps`의 `%CPU`는 OS가 관찰한 순간 CPU 사용률이고, 앱 로그의 `Current Load`는 앱 내부 부하 목표 또는 계산값입니다. 두 값이 완전히 같을 필요는 없기 때문에, 로그와 OS 관측치를 분리해서 해석했습니다.

## 7. Case 3: Deadlock 설명 스크립트

### 발표용 설명

```text
Deadlock 케이스에서는 MULTI_THREAD_ENABLE=true와 false를 비교했습니다.
true에서는 앱이 POTENTIAL DEADLOCK 경고를 출력했지만, ps -L과 /proc/<PID>/status로 확인한 실제 작업 프로세스의 Threads 값은 1이었습니다.
또한 WAITING, BLOCKED, lock 관련 로그도 없었고 CpuWorker 로그가 계속 진행되었습니다.
따라서 오늘 원본 앱 기준으로는 Deadlock이 재현됐다고 말할 수 없고, 경고 문구만 출력된 상태라고 판단했습니다.
false에서는 경고 문구가 사라졌지만 스레드 수는 마찬가지로 1개였습니다.
```

### 핵심 증거

앱 로그:

```text
[ THREAD ] Concurrency: True          [ WARNING ]
>>> SYSTEM WARNING: POTENTIAL DEADLOCK IN CONCURRENT MODE.

2026-06-22 17:19:28,351 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:19:31,469 [INFO] [CpuWorker] Current Load: 10.27%
2026-06-22 17:19:37,708 [INFO] [CpuWorker] Current Load: 21.62%
```

스레드 증거:

```text
# /proc/3455/status
State: S (sleeping)
VmRSS: 18720 kB
Threads: 1

# ps -L
PID   TID  STAT %CPU %MEM COMMAND
3455 3455  SN    0.5  0.1 agent-leak-app
```

### OS 개념 설명

Deadlock은 여러 스레드가 서로 상대방이 가진 자원을 기다리며 영원히 진행하지 못하는 상태입니다. 전형적인 조건은 상호 배제, 점유 대기, 비선점, 순환 대기입니다. 하지만 오늘 결과에서는 스레드가 1개였기 때문에 스레드 간 순환 대기를 증명할 수 없었습니다. 그래서 “Deadlock 재현 성공”이 아니라 “원본 앱에서 Deadlock 미재현”으로 판단했습니다.

## 8. 평가 질문 답변 자료

### Q1. monitor.sh에서 메모리 증가 패턴은 어떻게 추적했나요?

`monitor.sh`는 `pgrep -x agent-leak-app`으로 정확히 앱 PID를 찾고, 각 PID에 대해 아래 명령을 2초마다 실행해 로그에 남깁니다.

```bash
ps -p "$PID" -o pid,ppid,user,%cpu,%mem,rss,stat,cmd --no-headers
```

여기서 `rss`는 Resident Set Size로 실제 물리 메모리에 올라와 있는 양을 KB 단위로 보여줍니다. OOM before에서는 RSS가 `18628KB`에서 `44232KB`로 증가했고, 직후 프로세스가 사라진 것을 확인했습니다. 앱 로그의 Heap 카운터와 OS의 RSS가 서로 다른 단위와 기준이라는 점도 같이 설명할 수 있습니다.

### Q2. CPU 사용률 확인에 어떤 도구와 옵션을 썼나요?

세 가지를 썼습니다.

```bash
ps -C agent-leak-app -o pid,ppid,user,%cpu,%mem,rss,stat,cmd
top -bn1 -p "$PID"
ps -L -p "$PID" -o pid,tid,stat,%cpu,%mem,comm
```

`ps -C`는 프로세스 이름으로 전체 부모/자식 프로세스를 확인하기 위해 사용했습니다. `top -bn1 -p`는 특정 PID의 순간 CPU 상태를 배치 모드로 한 번 캡처하기 위해 사용했습니다. `ps -L`은 프로세스 내부 스레드별 상태를 확인하기 위해 사용했습니다.

### Q3. 살아있지만 멈춰있는 상태는 어떤 순서로 진단하나요?

먼저 `pgrep` 또는 `ps -ef`로 PID가 살아있는지 확인합니다. 그 다음 `monitor.sh`와 `ps`로 CPU/RSS가 계속 변하는지 봅니다. 마지막으로 `ps -L`, `top -H`, `/proc/<PID>/status`로 스레드 수와 상태를 확인합니다. 로그의 마지막 줄이 `WAITING`, `BLOCKED`, lock 대기라면 Deadlock 가능성이 높습니다. 오늘 원본 앱에서는 PID는 있었지만 스레드가 1개였고 로그가 계속 진행되어 Deadlock으로 확정하지 않았습니다.

### Q4. 메모리 보호 정책은 왜 프로세스를 종료하나요?

메모리 누수가 계속되면 해당 프로세스뿐 아니라 같은 서버의 다른 프로세스와 OS 전체가 메모리 부족 영향을 받습니다. 그래서 앱 내부 MemoryGuard는 설정한 한계에 도달하면 자기 프로세스를 종료해 장애 범위를 제한합니다. 이 조치는 임시 보호 장치이고, 근본 해결은 누수되는 객체를 해제하거나 캐시/버퍼 크기를 제한하는 것입니다.

### Q5. CPU 과점유 시 단일 프로세스를 종료하거나 제한하는 이유는 무엇인가요?

CPU는 여러 프로세스가 공유하는 자원입니다. 하나의 프로세스가 CPU를 계속 점유하면 다른 요청 처리, 로그 수집, SSH 접속, 모니터링 같은 운영 작업까지 느려질 수 있습니다. 그래서 Watchdog이나 rate limit을 통해 특정 프로세스의 CPU 사용량을 제한하거나 종료하는 것이 시스템 전체 안정성 측면에서 필요합니다. 오늘 원본 앱에서는 종료 대신 cooldown 방식이 관찰됐습니다.

### Q6. Deadlock을 상호 배제와 순환 대기로 설명해보세요.

상호 배제는 하나의 자원을 한 번에 하나의 스레드만 사용할 수 있는 조건입니다. 순환 대기는 Thread-A가 Thread-B의 자원을 기다리고, Thread-B가 Thread-A의 자원을 기다리는 식으로 대기 관계가 원형을 이루는 상태입니다. 이 상태에서는 아무도 자원을 놓지 않기 때문에 진행이 멈춥니다. 다만 오늘 원본 앱에서는 실제 스레드가 1개였기 때문에 순환 대기 증거가 없었습니다.

### Q7. 로그에서 스레드 간 순환 의존을 어떻게 파악하나요?

정상적인 Deadlock 증거라면 마지막 로그에 다음과 같은 관계가 보여야 합니다.

```text
Thread-A: Lock-1 획득 후 Lock-2 대기
Thread-B: Lock-2 획득 후 Lock-1 대기
```

이 경우 A는 B가 가진 Lock-2를 기다리고, B는 A가 가진 Lock-1을 기다리므로 순환 의존입니다. 오늘 원본 앱 로그에는 이런 `WAITING` 또는 `BLOCKED` 로그가 없어서 순환 의존을 입증하지 않았습니다.

### Q8. 실제 운영 서버라면 monitor.sh를 어떻게 개선하겠나요?

현재는 2초마다 스냅샷을 파일에 기록합니다. 운영용으로는 다음을 추가하겠습니다.

- RSS 증가율 계산: 최근 N분 동안 RSS가 계속 증가하면 경고
- 임계치 알림: `MEMORY_LIMIT`의 70%, 90%, 100% 도달 시 단계별 경고
- 부모/자식 PID 분리: 실제 부하를 쓰는 자식 프로세스까지 추적
- 로그 로테이션: 장시간 실행 시 로그 파일 과대 성장 방지
- JSON/CSV 출력: 그래프화와 후처리를 쉽게 함
- 알림 연동: Slack, 메일, GitHub Issue 자동 생성

### Q9. OOM, CPU Spike, Deadlock 중 실제 서비스에서 가장 치명적인 것은?

상황에 따라 다르지만, 저는 Deadlock이 가장 탐지하기 까다롭다고 설명하겠습니다. OOM과 CPU Spike는 자원 수치가 크게 변해서 모니터링으로 잡기 쉽습니다. Deadlock은 PID가 살아 있고 포트도 열려 있을 수 있어서 단순 프로세스 생존 체크만으로는 정상처럼 보일 수 있습니다. 예방하려면 lock 획득 순서를 통일하고, lock timeout을 두고, 스레드 덤프와 health check를 운영 모니터링에 포함해야 합니다.

### Q10. OOM과 Deadlock이 동시에 발생하면 어떤 순서로 보나요?

먼저 시스템 전체 안정성에 영향을 주는 OOM 여부를 봅니다. 메모리 부족은 OS 전체를 불안정하게 만들 수 있기 때문에 `free`, `ps --sort=-rss`, `/proc/<PID>/status`로 가장 큰 메모리 사용 프로세스를 확인합니다. 그 다음 PID가 살아 있는데 응답이 없는 프로세스에 대해 `ps -L`, `top -H`, 마지막 로그를 확인해 Deadlock 여부를 봅니다. 즉, 시스템 자원 고갈을 먼저 안정화하고, 그 다음 애플리케이션 내부 정지를 분석합니다.

### Q11. 소스 코드를 수정할 수 있다면 어떻게 개선하겠나요?

| 장애 | 코드 레벨 개선 |
|---|---|
| OOM | 사용 후 객체 해제, 캐시 크기 제한, 스트리밍 처리, 메모리 사용량 테스트 추가 |
| CPU Spike | busy-loop 제거, 작업 큐 rate limit, CPU 집약 작업 분리, 타임아웃과 backoff 적용 |
| Deadlock | lock 획득 순서 통일, lock timeout, try-lock 실패 처리, 스레드 덤프 로깅 |

### Q12. 다시 수행한다면 무엇을 다르게 하겠나요?

처음부터 원본 바이너리와 시뮬레이터 결과를 분리해서 기록하겠습니다. 또한 각 케이스마다 실행 시작 전 환경변수, 바이너리 SHA-256, PID, 앱 로그, monitor 로그, `ps/top/proc` 스냅샷을 같은 타임스탬프로 묶어 증거 패키지를 만들겠습니다. 그러면 평가자가 어떤 로그가 어떤 실행에서 나온 것인지 더 쉽게 검증할 수 있습니다.

## 9. 평가 때 주의할 표현

사용해도 좋은 표현:

```text
원본 앱에서 실제 관찰한 결과는 교재 예시와 일부 달랐습니다.
그래서 기대 로그를 임의로 만들지 않고, 관찰된 로그와 OS 명령 출력만 근거로 판단했습니다.
CPU는 Watchdog 종료 대신 cooldown이 관찰됐고, Deadlock은 스레드 1개라 재현 성공으로 보지 않았습니다.
```

피해야 할 표현:

```text
CPU Watchdog이 발동했습니다.
Deadlock이 발생했습니다.
WAITING/BLOCKED 로그를 확인했습니다.
```

위 표현은 오늘 원본 실행 증거와 맞지 않습니다.

## 10. 30초 마무리 멘트

```text
이번 미션에서 저는 원본 agent-leak-app-x86를 실행하고, 로그와 OS 명령어 출력을 근거로 세 가지 장애를 분석했습니다.
OOM은 MemoryGuard 자기 종료가 명확히 재현됐습니다.
CPU는 임계치에 따라 cooldown 동작이 달라졌지만 Watchdog 종료는 원본 앱에서 재현되지 않았습니다.
Deadlock은 경고 문구는 있었지만 실제 스레드가 1개이고 lock 대기 로그가 없어 미재현으로 판단했습니다.
결론적으로, 미션의 핵심인 관제 데이터 기반 판단과 GitHub Issue 형식 보고는 수행했고, 원본 앱이 교재 예시와 다르게 동작한 부분도 증거로 남겼습니다.
```
