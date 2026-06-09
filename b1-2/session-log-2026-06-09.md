# B1-2 미션 세션 로그 — 2026-06-09

## 개요

- **미션:** B1-2 리눅스 프로세스 및 시스템 리소스 트러블슈팅
- **목표:** 3가지 장애(Memory Leak / CPU Spike / Deadlock)를 재현하고 GitHub Issue 보고서 작성
- **환경:** macOS + OrbStack + Ubuntu 22.04 (b1-2 VM)

---

## 주요 작업 내역

### 1. agent-leak-sim.py 개발

원본 `agent-leak-app` 바이너리 대신, 학습용 PC(sudo 제한 환경)에서도 동작하는 Python 시뮬레이터를 직접 제작.

**파일:** `b1-2/agent-leak-sim.py`

**핵심 기능:**
- 대화형 케이스 선택 메뉴 (1/2/3)
- 케이스별 환경변수 프리셋 자동 적용
- 실제 메모리 할당 (`bytearray`), 실제 CPU 번 (`math.sqrt` busy-loop)
- 실제 스레드 교착 (`threading.Lock` 순환 대기)
- 로그 경로 자동 결정: `/var/log/agent-app/` (VM) 또는 `./logs/` (macOS fallback)

**실행 방법:**
```bash
cd /Users/cspag5955/Documents/AI-SW-Basic/b1-2
python3 agent-leak-sim.py
```

**케이스별 프리셋:**

| 케이스 | MEMORY_LIMIT | CPU_MAX_OCCUPY | MULTI_THREAD_ENABLE |
|--------|-------------|----------------|----------------------|
| 1 (Memory Leak) | 256 MB | 100 % | false |
| 2 (CPU Spike)   | 9999 MB | 50 % | false |
| 3 (Deadlock)    | 9999 MB | 100 % | true |

---

### 2. Case 1 — Memory Leak 분석

**관찰 내용:**
- UP 모드에서 메모리가 +25MB/step으로 증가
- 250MB까지 도달 후 DOWN 모드 진입 (메모리 해제 없음 = 누수)
- 다음 UP 사이클 첫 스텝에서 275MB ≥ 256MB → MemoryGuard 발동

**종료 메시지:**
```
[CRITICAL] [MemoryGuard] Memory limit exceeded (275MB >= 256MB)
[CRITICAL] [MemoryGuard] Self-terminating process XXXX to prevent system instability.
>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<
```

**보고서:** `b1-2/report-case1-memory-leak.md` → GitHub Issue 생성 완료

---

### 3. Case 2 — CPU Spike 분석

**관찰 내용:**
- UP 모드에서 CPU 레벨 상승 (Lv=1~10, 레벨×0.5초 busy-loop)
- Lv=8 도달 시 실제 CPU% 측정: 99.7% > CPU_MAX_OCCUPY(50%)
- Watchdog 발동 → 프로세스 종료

**종료 메시지:**
```
[WARNING] [Watchdog] CPU usage spike detected: 99.7% > 50%
[CRITICAL] [Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)
>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<
```

**보고서:** `b1-2/report-case2-cpu-spike.md` → GitHub Issue 생성 필요

---

### 4. Case 3 — Deadlock 분석

**관찰 내용:**
- MULTI_THREAD_ENABLE=true 상태로 1 사이클(UP+DOWN) 완료 후 Deadlock 트리거
- Thread-A: Lock-1 획득 → Lock-2 대기
- Thread-B: Lock-2 획득 → Lock-1 대기
- 순환 대기 → 로그 완전 정지, 프로세스는 생존

**마지막 로그:**
```
2026-06-09 17:45:28 [INFO] [Thread-A] Acquired Lock-1, WAITING for Lock-2...
2026-06-09 17:45:28 [INFO] [Thread-B] Acquired Lock-2, WAITING for Lock-1...
(이후 로그 없음)
```

**프로세스 확인:**
```
PID 28648  Python agent-leak-sim.py  TIME: 0:55.09 (변화 없음)
```

**보고서:** `b1-2/report-case3-deadlock.md` → GitHub Issue 생성 필요

---

## 생성/수정된 파일 목록

| 파일 | 설명 |
|------|------|
| `b1-2/agent-leak-sim.py` | 장애 시뮬레이터 (신규) |
| `b1-2/report-case1-memory-leak.md` | Case 1 보고서 |
| `b1-2/report-case2-cpu-spike.md` | Case 2 보고서 |
| `b1-2/report-case3-deadlock.md` | Case 3 보고서 |
| `b1-2/session-log-2026-06-09.md` | 이 파일 |

---

## 남은 작업

- [ ] Case 2 GitHub Issue 생성 — https://github.com/linksat1/AI-SW-Basic/issues
- [ ] Case 3 GitHub Issue 생성 — https://github.com/linksat1/AI-SW-Basic/issues
- [ ] 최종 제출: GitHub Repository 링크 또는 Issue 3건 PDF 캡처
