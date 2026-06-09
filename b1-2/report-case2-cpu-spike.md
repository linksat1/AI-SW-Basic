# [Bug] CPU 과점유로 인한 Watchdog 긴급 종료

## 1. Description (현상 설명)

- **현상:** agent-leak-app 실행 중 CPU 레벨이 최고치(Lv=10)에 반복 도달하며 CPU를 과점유
- **조건:** CPU_MAX_OCCUPY=50, MEMORY_LIMIT=256, MULTI_THREAD_ENABLE=true
- **환경:** Ubuntu 22.04 (OrbStack VM), agent-admin 계정

## 2. Evidence & Logs (증거 자료)

### agent_app.log — CPU Lv=10 반복 발생 패턴

```
2026-06-09 15:38:19 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-06-09 15:38:25 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-06-09 15:40:01 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-06-09 15:40:07 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
2026-06-09 15:41:43 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=225MB ---
2026-06-09 15:41:49 [INFO] --- Step Info: Mode=UP, CPU Lv=10, Mem=250MB ---
```

### ps 모니터링 — CPU 사용률

```
PID   COMMAND         %CPU  %MEM
15527 agent-leak-app  15.7  1.9
```

### CPU Lv=10 발생 주기

| 발생 시각 | CPU 레벨 | 메모리 |
|----------|---------|--------|
| 15:38:19 | Lv=10 | 225MB |
| 15:40:01 | Lv=10 | 225MB |
| 15:41:43 | Lv=10 | 225MB |
| 15:43:26 | Lv=10 | 225MB |
| 주기 | **약 1분 42초마다 반복** | |

## 3. Root Cause Analysis (원인 분석)

- 앱 내부 CPU 점유 로직이 레벨(1~10)에 따라 코어를 독점하는 방식으로 동작
- Lv=10에서 5초간 CPU 코어를 완전 점유 → CPU_MAX_OCCUPY(50%) 임계치 초과 위험
- 약 1분 42초 주기로 반복 발생하여 시스템 전체 성능에 영향

## 4. Workaround & Verification (조치 및 검증)

- **조치:** CPU_MAX_OCCUPY 값을 50 → 80으로 상향 조정
- **Before:** CPU_MAX_OCCUPY=50 → Lv=10 도달 시 임계치 초과
- **After:** CPU_MAX_OCCUPY=80 → 더 높은 CPU 사용률 허용으로 안정적 동작
- **근본 해결:** CPU 점유 로직에 시간 제한 및 양보(yield) 처리 추가 필요

## 5. 관련 환경변수

```bash
AGENT_HOME=/home/agent-admin/agent-app
MEMORY_LIMIT=256
CPU_MAX_OCCUPY=50
MULTI_THREAD_ENABLE=true
```
