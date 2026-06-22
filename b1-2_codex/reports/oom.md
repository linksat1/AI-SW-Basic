# [Bug] Memory Leak / OOM - MEMORY_LIMIT 초과 시 MemoryGuard 자기 종료 확인

## 1. Description (현상 설명)

- **발생 현상:** `MEMORY_LIMIT=50` 조건에서 앱 내부 Heap이 50MB에 도달하자 MemoryGuard가 한계 초과를 감지하고 프로세스를 종료했다.
- **발생 조건:** OrbStack Ubuntu `b1-lab`, `agent-admin`, 원본 `agent-leak-app-x86`.
- **실행 환경:** `/home/agent-admin/agent-app`, 로그 디렉터리 `/var/log/agent-app`, 포트 `15034`.
- **관련 환경변수:**

```text
Before: MEMORY_LIMIT=50, CPU_MAX_OCCUPY=100, MULTI_THREAD_ENABLE=false
After : MEMORY_LIMIT=512, CPU_MAX_OCCUPY=100, MULTI_THREAD_ENABLE=false
```

- **기대 동작:** 낮은 메모리 한계에서 메모리 증가가 관찰되고, 한계 초과 시 보호 정책으로 종료된다.
- **실제 동작:** Before에서는 `Memory limit exceeded`와 `Self-terminating process` 로그가 발생했다. After에서는 제한 시간 동안 종료 로그 없이 CPU Worker 로그가 계속 기록됐다.

## 2. Evidence & Logs (증거 자료)

### 2-1. 앱 실행 로그

```text
2026-06-22 17:18:00,605 [INFO] [MemoryWorker] Current Heap: 25MB
2026-06-22 17:18:03,656 [INFO] [MemoryWorker] Current Heap: 50MB
2026-06-22 17:18:03,657 [CRITICAL] [MemoryGuard] Memory limit exceeded (50MB >= 50MB) / (Recommend Over 256MB)
2026-06-22 17:18:03,657 [CRITICAL] [MemoryGuard] Self-terminating process 3114 to prevent system instability.
```

### 2-2. 모니터링 로그

```text
[Mon Jun 22 17:18:02 KST 2026] --- Monitor Snapshot ---
PROCESS: OK - agent-leak-app running with PID(s): 3104
3114
   3114    3104 agent-a+  1.5  0.2 44232 SN   ./agent-leak-app
PORT: OK - 15034 is listening

[Mon Jun 22 17:18:04 KST 2026] --- Monitor Snapshot ---
PROCESS: FAIL - agent-leak-app is NOT running
PORT: WARN - 15034 is not listening
```

### 2-3. 시스템 명령어 출력

```text
# ps snapshot for oom_before at Mon Jun 22 17:18:05 KST 2026
agent-leak-app not running at snapshot time
```

## 3. Root Cause Analysis (원인 분석)

- 관찰된 증거 1: 앱 로그에서 Heap이 25MB에서 50MB로 증가했다.
- 관찰된 증거 2: `MEMORY_LIMIT=50`에 도달하자 MemoryGuard가 즉시 CRITICAL 로그를 남겼다.
- 추론한 원인: 메모리 증가 워커가 주기적으로 Heap을 늘리고, 앱 내부 MemoryGuard가 설정된 `MEMORY_LIMIT`과 내부 Heap 카운터를 비교해 자기 종료했다.
- 관련 OS 개념: 프로세스 RSS는 `ps`/`monitor.sh`로 관찰하고, 앱 내부 Heap 카운터는 앱 로그로 관찰한다. 이번 케이스는 앱 내부 보호 로직의 자기 종료가 핵심 증거다.
- 원본 앱 기준 해석: OOM 케이스는 미션 설명과 일치하게 재현됐다.

## 4. Workaround & Verification (조치 및 검증)

### 4-1. 조치 내용

```text
변경 전: MEMORY_LIMIT=50
변경 후: MEMORY_LIMIT=512
```

### 4-2. Before & After 비교

| 항목 | Before | After |
|---|---|---|
| 환경변수 | `MEMORY_LIMIT=50` | `MEMORY_LIMIT=512` |
| 관찰 결과 | Heap 50MB 도달 후 MemoryGuard 발동 | 제한 시간 동안 종료 로그 없음 |
| 종료 여부 | 자기 종료 확인 | 제한 시간 종료 전까지 실행 지속 |
| 핵심 로그 | `Memory limit exceeded`, `Self-terminating process` | `Current Load` 로그 지속 |

### 4-3. 결론

- 임시 조치 효과: `MEMORY_LIMIT`을 512MB로 높이면 관찰 시간 내 MemoryGuard 종료가 발생하지 않았다.
- 남은 위험: 실제 서비스에서는 Heap 증가 원인을 제거하지 않으면 더 높은 한계에서도 장시간 실행 시 문제가 재발할 수 있다.
- 근본 해결 제안: MemoryWorker가 할당한 객체를 해제하거나 작업 단위별 메모리 상한을 적용한다.
- 원본 앱 기준 최종 판단: Memory Leak / OOM 재현 성공.

## 5. 첨부/참조 증거

- `evidence/logs/oom_before_app.log`
- `evidence/logs/oom_before_monitor.log`
- `evidence/logs/oom_before_ps.log`
- `evidence/logs/oom_after_app.log`
- `evidence/logs/oom_after_monitor.log`
- `evidence/logs/oom_after_ps.log`
