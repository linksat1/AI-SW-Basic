# [Bug] CPU Spike - CPU_MAX_OCCUPY 변경 시 CpuWorker cooldown 동작 확인

## 1. Description (현상 설명)

- **발생 현상:** `CPU_MAX_OCCUPY=10` 조건에서 CpuWorker가 10%에 도달하면 Watchdog/SIGTERM 종료가 아니라 cooldown으로 부하를 낮춘 뒤 다시 증가시켰다.
- **발생 조건:** OrbStack Ubuntu `b1-lab`, `agent-admin`, 원본 `agent-leak-app-x86`.
- **실행 환경:** `/home/agent-admin/agent-app`, 로그 디렉터리 `/var/log/agent-app`, 포트 `15034`.
- **관련 환경변수:**

```text
Before: MEMORY_LIMIT=512, CPU_MAX_OCCUPY=10, MULTI_THREAD_ENABLE=false
After : MEMORY_LIMIT=512, CPU_MAX_OCCUPY=50, MULTI_THREAD_ENABLE=false
```

- **기대 동작:** CPU 임계치 초과 시 Watchdog 또는 SIGTERM 종료가 발생한다.
- **실제 동작:** `CPU_MAX_OCCUPY=10`에서는 `Peak reached`와 `Cooldown complete`가 반복됐고, `WATCHDOG`, `SIGTERM` 로그는 관찰되지 않았다. `CPU_MAX_OCCUPY=50`에서는 관찰 시간 동안 부하가 24.78%까지 증가했다.

## 2. Evidence & Logs (증거 자료)

### 2-1. 앱 실행 로그

```text
2026-06-22 17:18:49,035 [INFO] [CpuWorker] Started. Maximum CPU Limit: 10%
2026-06-22 17:18:49,035 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:18:51,146 [INFO] [CpuWorker] Peak reached (10.00%). Starting cooldown...
2026-06-22 17:18:52,151 [INFO] [CpuWorker] Current Load: 10.00%
2026-06-22 17:18:57,376 [INFO] [CpuWorker] Cooldown complete (5.00%). Resuming load increase...
```

After 비교:

```text
2026-06-22 17:19:09,079 [INFO] [CpuWorker] Current Load: 5.00%
2026-06-22 17:19:12,191 [INFO] [CpuWorker] Current Load: 5.74%
2026-06-22 17:19:15,307 [INFO] [CpuWorker] Current Load: 12.71%
2026-06-22 17:19:18,421 [INFO] [CpuWorker] Current Load: 22.66%
2026-06-22 17:19:21,539 [INFO] [CpuWorker] Current Load: 24.78%
```

### 2-2. 모니터링 로그

```text
[Mon Jun 22 17:18:58 KST 2026] --- Monitor Snapshot ---
PROCESS: OK - agent-leak-app running with PID(s): 3252
3262
   3262    3252 agent-a+  1.9  0.7 121384 SNl ./agent-leak-app
PORT: OK - 15034 is listening
```

### 2-3. 시스템 명령어 출력

```text
# ps snapshot for cpu_before at Mon Jun 22 17:18:53 KST 2026
    PID    PPID USER     %CPU %MEM   RSS STAT CMD
   3262    3252 agent-a+  2.0  0.4 70176 SNl  ./agent-leak-app

Threads: 3
```

## 3. Root Cause Analysis (원인 분석)

- 관찰된 증거 1: 앱 로그의 `Current Load`가 `CPU_MAX_OCCUPY=10`에 맞춰 10% 근처에서 `Peak reached`로 전환됐다.
- 관찰된 증거 2: `WATCHDOG`, `SIGTERM`, `CPU Threshold Violated` 로그는 수집 로그에서 발견되지 않았다.
- 추론한 원인: 원본 앱의 CPU 케이스는 강제 종료 Watchdog보다 CpuWorker의 자체 부하 조절과 cooldown 경로가 우선 동작한다.
- 관련 OS 개념: `ps`의 `%CPU`는 순간 OS 관측값이고, 앱 로그의 `Current Load`는 앱 내부 부하 목표 또는 계산값이다. 둘은 동일한 지표가 아니다.
- 원본 앱 기준 해석: CPU 부하 상승과 임계치별 cooldown은 재현됐지만, Watchdog/SIGTERM 종료는 재현되지 않았다.

## 4. Workaround & Verification (조치 및 검증)

### 4-1. 조치 내용

```text
변경 전: CPU_MAX_OCCUPY=10
변경 후: CPU_MAX_OCCUPY=50
```

### 4-2. Before & After 비교

| 항목 | Before | After |
|---|---|---|
| 환경변수 | `CPU_MAX_OCCUPY=10` | `CPU_MAX_OCCUPY=50` |
| 관찰 결과 | 10% 도달 후 cooldown 반복 | 24.78%까지 증가, cooldown 미도달 |
| 종료 여부 | Watchdog 종료 없음 | Watchdog 종료 없음 |
| 핵심 로그 | `Peak reached`, `Cooldown complete` | `Current Load` 증가 |

### 4-3. 결론

- 임시 조치 효과: `CPU_MAX_OCCUPY`를 높이면 낮은 임계치에서 발생하던 cooldown이 관찰 시간 내 발생하지 않았다.
- 남은 위험: Watchdog 종료가 필요하다면 현재 원본 앱 동작은 미션 설명과 다르다.
- 근본 해결 제안: CPU Watchdog 요구사항이 있다면 `%CPU` 실측값 기준으로 임계치 초과 시 SIGTERM을 보내는 로직을 별도로 검증해야 한다.
- 원본 앱 기준 최종 판단: CPU Spike 자체는 재현됐지만 Watchdog/SIGTERM 종료는 재현되지 않음.

## 5. 첨부/참조 증거

- `evidence/logs/cpu_before_app.log`
- `evidence/logs/cpu_before_monitor.log`
- `evidence/logs/cpu_before_ps.log`
- `evidence/logs/cpu_after_app.log`
- `evidence/logs/cpu_after_monitor.log`
- `evidence/logs/cpu_after_ps.log`
