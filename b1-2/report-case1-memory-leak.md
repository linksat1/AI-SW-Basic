# [Bug] 메모리 누수로 인한 MemoryGuard 보호 정책 강제 종료

## 1. Description (현상 설명)

- **현상:** agent-leak-app 실행 후 메모리가 25MB씩 지속 증가하여 MEMORY_LIMIT(256MB)을 초과함
- **조건:** MEMORY_LIMIT=256, CPU_MAX_OCCUPY=50, MULTI_THREAD_ENABLE=true
- **환경:** Ubuntu 22.04 (OrbStack VM), agent-admin 계정

## 2. Evidence & Logs (증거 자료)

### agent_app.log — 메모리 상승 패턴

```
2026-06-09 09:34:48 [INFO] >>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<
2026-06-09 09:34:48 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-06-09 09:34:50 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
2026-06-09 09:34:53 [INFO] [Memory] Increasing... (+25 MB) Total: 75 MB
2026-06-09 09:34:57 [INFO] [Memory] Increasing... (+25 MB) Total: 100 MB
2026-06-09 09:35:02 [INFO] [Memory] Increasing... (+25 MB) Total: 125 MB
2026-06-09 09:35:08 [INFO] [Memory] Increasing... (+25 MB) Total: 150 MB
2026-06-09 09:35:14 [INFO] [Memory] Increasing... (+25 MB) Total: 175 MB
2026-06-09 09:35:20 [INFO] [Memory] Increasing... (+25 MB) Total: 200 MB
2026-06-09 09:35:26 [INFO] [Memory] Increasing... (+25 MB) Total: 225 MB
2026-06-09 09:35:32 [INFO] [Memory] Increasing... (+25 MB) Total: 250 MB
2026-06-09 09:35:38 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB  ← MEMORY_LIMIT(256MB) 초과
```

### 메모리 상승 속도

| 구간 | 시간 | 증가량 |
|------|------|--------|
| 0MB → 275MB | 약 50초 | +25MB/단계 |
| MEMORY_LIMIT 초과 | 256MB 이후 | 계속 증가 |

## 3. Root Cause Analysis (원인 분석)

- 앱 내부에서 메모리를 할당 후 해제하지 않는 **메모리 누수(Memory Leak)** 발생
- 메모리가 25MB 단위로 계속 할당되어 MEMORY_LIMIT(256MB)를 초과
- 정상 동작: 메모리 할당 → 사용 → 해제 (일정하게 유지)
- 누수 동작: 메모리 할당 → 사용 → **[해제 안 함]** → 계속 증가

## 4. Workaround & Verification (조치 및 검증)

- **조치:** MEMORY_LIMIT을 256MB → 512MB로 상향 조정
- **Before:** MEMORY_LIMIT=256 → 약 50초 후 한계 도달
- **After:** MEMORY_LIMIT=512 → 더 오랜 시간 생존 확인
- **근본 해결:** 소스코드에서 불필요한 데이터를 주기적으로 해제하는 리팩토링 필요

## 5. 관련 환경변수

```bash
AGENT_HOME=/home/agent-admin/agent-app
MEMORY_LIMIT=256
CPU_MAX_OCCUPY=50
MULTI_THREAD_ENABLE=true
```
