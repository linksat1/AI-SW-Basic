# [Bug] Deadlock - MULTI_THREAD_ENABLE=true에서도 실제 데드락 미재현

## 1. Description (현상 설명)

- **발생 현상:** `MULTI_THREAD_ENABLE=true` 조건에서 앱은 `POTENTIAL DEADLOCK` 경고를 출력했지만, OS 관측상 실제 작업 프로세스의 스레드는 1개였고 `WAITING`, `BLOCKED`, lock 관련 로그는 관찰되지 않았다.
- **발생 조건:** OrbStack Ubuntu `b1-lab`, `agent-admin`, 원본 `agent-leak-app-x86`.
- **실행 환경:** `/home/agent-admin/agent-app`, 로그 디렉터리 `/var/log/agent-app`, 포트 `15034`.
- **관련 환경변수:**

```text
Before: MEMORY_LIMIT=512, CPU_MAX_OCCUPY=100, MULTI_THREAD_ENABLE=true
After : MEMORY_LIMIT=512, CPU_MAX_OCCUPY=100, MULTI_THREAD_ENABLE=false
```

- **기대 동작:** 멀티스레드 활성화 시 데드락으로 PID는 살아 있으나 로그/CPU/MEM 변화가 멈춘다.
- **실제 동작:** Before에서 경고 문구는 출력됐지만 `Threads: 1`로 확인됐고, CpuWorker 로그가 계속 증가했다. After도 단일 스레드로 유사하게 실행됐다.

## 2. Evidence & Logs (증거 자료)

### 2-1. 앱 실행 로그

```text
[ THREAD ] Concurrency: True          [ WARNING ]
--------------------------------------------------
 >>> SYSTEM WARNING: POTENTIAL DEADLOCK IN CONCURRENT MODE.
==================================================

2026-06-22 17:19:28,350 [INFO] [CpuWorker] Started. Maximum CPU Limit: 100%
2026-06-22 17:19:28,351 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:19:31,469 [INFO] [CpuWorker] Current Load: 10.27%
2026-06-22 17:19:34,589 [INFO] [CpuWorker] Current Load: 12.04%
2026-06-22 17:19:37,708 [INFO] [CpuWorker] Current Load: 21.62%
```

### 2-2. 모니터링 로그

```text
[Mon Jun 22 17:19:42 KST 2026] --- Monitor Snapshot ---
PROCESS: OK - agent-leak-app running with PID(s): 3445
3455
   3455    3445 agent-a+  0.7  0.1 18720 SN   ./agent-leak-app
PORT: OK - 15034 is listening
```

### 2-3. 시스템 명령어 출력

```text
# /proc/3455/status
Name: agent-leak-app
State: S (sleeping)
VmRSS: 18720 kB
Threads: 1

# thread snapshot
    PID     TID STAT %CPU %MEM COMMAND
   3455    3455 SN    0.5  0.1 agent-leak-app
```

## 3. Root Cause Analysis (원인 분석)

- 관찰된 증거 1: 앱은 `POTENTIAL DEADLOCK IN CONCURRENT MODE` 경고를 출력했다.
- 관찰된 증거 2: `/proc/<PID>/status`와 `ps -L` 결과에서 실제 작업 프로세스는 `Threads: 1`이었다.
- 관찰된 증거 3: Deadlock 조건에서 기대되는 `WAITING`, `BLOCKED`, lock 로그가 없고 CpuWorker 로그가 계속 증가했다.
- 추론한 원인: 원본 앱의 `MULTI_THREAD_ENABLE=true`는 경고 메시지 출력에는 반영되지만, 관찰 시점의 실제 작업 경로에서는 데드락을 만들 다중 스레드 또는 lock 대기 상태가 활성화되지 않았다.
- 관련 OS 개념: 데드락 판단에는 PID 생존만으로 부족하며, 스레드 상태와 로그 진행 정지가 함께 필요하다.
- 원본 앱 기준 해석: Deadlock은 재현되지 않았고, 미션 설명과 원본 앱 관찰 결과가 다르다.

## 4. Workaround & Verification (조치 및 검증)

### 4-1. 조치 내용

```text
변경 전: MULTI_THREAD_ENABLE=true
변경 후: MULTI_THREAD_ENABLE=false
```

### 4-2. Before & After 비교

| 항목 | Before | After |
|---|---|---|
| 환경변수 | `MULTI_THREAD_ENABLE=true` | `MULTI_THREAD_ENABLE=false` |
| 관찰 결과 | Deadlock 경고 출력, 실제 Threads 1 | Deadlock 경고 없음, 실제 Threads 1 |
| 종료 여부 | 제한 시간 동안 실행 | 제한 시간 동안 실행 |
| 핵심 로그 | `POTENTIAL DEADLOCK`, `Current Load` 증가 | `Current Load` 증가 |

### 4-3. 결론

- 임시 조치 효과: `MULTI_THREAD_ENABLE=false`는 경고 문구를 제거하지만, 실제 스레드 수는 before/after 모두 1개였다.
- 남은 위험: 원본 앱만으로는 Deadlock 장애를 증명할 충분한 lock 대기 증거가 없다.
- 근본 해결 제안: 데드락 재현 요구사항이 있다면 실제로 두 개 이상의 스레드가 동일 lock을 교차 대기하는 코드 경로를 확인해야 한다.
- 원본 앱 기준 최종 판단: Deadlock 미재현.

## 5. 첨부/참조 증거

- `evidence/logs/deadlock_before_app.log`
- `evidence/logs/deadlock_before_monitor.log`
- `evidence/logs/deadlock_before_ps.log`
- `evidence/logs/deadlock_after_app.log`
- `evidence/logs/deadlock_after_monitor.log`
- `evidence/logs/deadlock_after_ps.log`
