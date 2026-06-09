# [Bug] 멀티스레드 환경에서 교착상태(Deadlock) 발생으로 프로세스 무응답

## 1. Description (현상 설명)

- **현상:** agent-leak-sim 실행 후 프로세스가 종료되지 않고 PID 유지
- **조건:** MULTI_THREAD_ENABLE=true, MEMORY_LIMIT=9999, CPU_MAX_OCCUPY=100
- **환경:** macOS (Python 3.9), agent-admin 계정

## 2. Evidence & Logs (증거 자료)

### agent_app.log — 교착 진입 지점 (마지막 로그)

```
2026-06-09 17:45:28 [INFO] [Thread-A] Acquired Lock-1, WAITING for Lock-2...
2026-06-09 17:45:28 [INFO] [Thread-B] Acquired Lock-2, WAITING for Lock-1...
(이후 로그 없음)
```

### ps -ef — 프로세스 살아있음 확인

```
PID   COMMAND                                    TIME
28648 Python agent-leak-sim.py                0:55.09
```

- PID 28648 존재 → 프로세스 종료되지 않음
- CPU 누적 시간 0:55.09 → 이후 변화 없음 (스레드 모두 대기 상태)

### 교착상태 발생 흐름

| 시각 | Thread-A | Thread-B |
|------|----------|----------|
| 17:45:28 | Lock-1 획득 → Lock-2 대기 | Lock-2 획득 → Lock-1 대기 |
| 17:45:28~ | **무한 대기** | **무한 대기** |

## 3. Root Cause Analysis (원인 분석)

- Thread-A: Lock-1 보유 → Lock-2 대기
- Thread-B: Lock-2 보유 → Lock-1 대기
- 교착상태 4대 조건 중 **순환 대기(Circular Wait)** 발생
  - 상호 배제: Lock은 한 스레드만 사용 가능
  - 점유 대기: 각 스레드가 락을 보유한 채 다른 락 대기
  - 비선점: 보유 중인 락을 강제로 빼앗을 수 없음
  - 순환 대기: A→B→A 순환 구조
- 두 스레드가 서로의 자원을 영원히 기다려 진행 불가 → 프로세스 무응답

## 4. Workaround & Verification (조치 및 검증)

- **조치:** MULTI_THREAD_ENABLE=false로 변경 (싱글스레드 모드)
- **Before:** true → 멀티스레드 → 교착상태 발생 → 무응답
- **After:** false → 싱글스레드 → 자원 경쟁 없음 → 정상 동작
- **근본 해결:** 락 획득 순서를 통일(Lock-1 → Lock-2 순서를 모든 스레드에 강제)하거나 타임아웃을 설정하는 코드 개선 필요

## 5. 관련 환경변수

```bash
AGENT_HOME=/home/agent-admin/agent-app
MEMORY_LIMIT=9999
CPU_MAX_OCCUPY=100
MULTI_THREAD_ENABLE=true
```
