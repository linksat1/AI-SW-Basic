# B1-2 과제 설명 자료 — 초보자용 정리

> 이 문서는 B1-2 미션 완료 후 "설명할 수 있어야 하는 내용"을 우리가 실제로 실행한
> 명령어·로그·결과와 연결하여 정리한 자료입니다.

---

## 0. 이 미션의 교육 목표

| 목표 | 의미 |
|---|---|
| 장애를 **눈으로 직접 재현** | "메모리 누수"라는 단어만 아는 것과, 실제로 메모리가 25MB씩 늘어나는 로그를 본 것은 다르다 |
| 로그를 **증거로 사용** | "왜 죽었지?"라는 질문에 감이 아니라 로그 한 줄로 답할 수 있어야 한다 |
| 원인 → 조치 → 검증의 **사이클** | 문제를 발견했으면, 설정을 바꿔보고, 그 결과를 다시 관찰해서 효과를 증명한다 |
| **GitHub Issue**로 문서화 | 혼자 알고 끝내는 게 아니라, 팀이 읽고 재현/검증/참고할 수 있는 기록을 남긴다 |

한 줄 요약: **"장애 = 감으로 추측하는 것"이 아니라 "장애 = 데이터로 증명하고 기록하는 것"** 으로 바꾸는 훈련.

---

## 1. 우리가 만든 도구 — agent-leak-sim.py

### 왜 직접 만들었나?

원본 `agent-leak-app`은 리눅스 바이너리이고, 실습 PC가 학습용이라 `sudo` 권한이 제한되어
`/var/log/agent-app/` 같은 시스템 경로에 자유롭게 쓸 수 없었습니다.
그래서 **같은 로그 패턴을 그대로 출력하는 Python 스크립트**를 만들어, sudo 없이도
세 가지 장애를 동일하게 재현했습니다.

### 실행 명령어

```bash
cd /Users/cspag5955/Documents/AI-SW-Basic/b1-2
python3 agent-leak-sim.py
```

| 명령 | 의미 |
|---|---|
| `cd 경로` | "change directory" — 작업할 폴더로 이동 |
| `python3 파일.py` | Python 3 인터프리터로 스크립트를 실행 |

실행하면 메뉴가 나오고, **1/2/3 번호 + Enter**만 누르면 해당 케이스에 맞는
환경변수(MEMORY_LIMIT, CPU_MAX_OCCUPY, MULTI_THREAD_ENABLE)가 자동으로 설정됩니다.

---

## 2. Case 1 — Memory Leak (메모리 누수)

### 2-1. 무슨 명령을 실행했나

```bash
python3 agent-leak-sim.py
# 메뉴에서 "1" 입력 → Enter (Memory Leak 프리셋 적용)
```

적용된 설정값:
```
MEMORY_LIMIT        = 256 MB
CPU_MAX_OCCUPY      = 100 %   (CPU 때문에 먼저 안 죽도록 높게 설정)
MULTI_THREAD_ENABLE = false   (Deadlock이 끼어들지 않도록 끔)
```

### 2-2. 실행 결과 (실제 로그)

```
2026-06-09 09:34:48 [INFO] [Memory] Increasing... (+25 MB) Total: 25 MB
2026-06-09 09:34:50 [INFO] [Memory] Increasing... (+25 MB) Total: 50 MB
...
2026-06-09 09:35:38 [INFO] [Memory] Increasing... (+25 MB) Total: 275 MB  ← 한계(256MB) 초과

[CRITICAL] [MemoryGuard] Memory limit exceeded (275MB >= 256MB)
[CRITICAL] [MemoryGuard] Self-terminating process XXXX to prevent system instability.
>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<
```

### 2-3. 로그 한 줄씩 해석

| 로그 | 의미 |
|---|---|
| `[Memory] Increasing... (+25 MB) Total: 275 MB` | 프로그램이 25MB짜리 메모리 덩어리를 또 할당했고, 누적이 275MB가 됐다는 뜻 |
| `[CRITICAL] [MemoryGuard] Memory limit exceeded` | "메모리 감시자(MemoryGuard)"가 한계(256MB)를 넘은 것을 감지 |
| `Self-terminating process XXXX` | 시스템 전체가 죽기 전에 **이 프로세스 스스로를 종료**시킨다는 뜻 (XXXX = 프로세스 번호 PID) |
| `SELF-TERMINATED` | 정상적으로 자기 자신을 종료했다는 시스템 메시지 |

### 2-4. 질문 1 — 메모리 누수가 시스템에 미치는 영향은?

> **메모리는 컴퓨터 전체가 같이 쓰는 자원**입니다.
> 도서관 책장에 비유하면, 누군가 책(메모리)을 계속 빌려가고 반납하지 않으면
> 결국 다른 사람이 빌릴 책이 없어집니다.
>
> 우리 실습에서는 한 프로그램이 25MB씩 계속 할당만 하고 해제하지 않아서
> 256MB라는 한계에 도달했고, 이때 `MemoryGuard`라는 보호 장치가
> "이대로 두면 시스템 전체(다른 프로그램들까지)가 멈출 수 있다"고 판단하여
> 이 프로그램을 강제 종료했습니다.
>
> 만약 이런 보호 장치가 없었다면, 운영체제(OS)가 직접 개입해서
> 메모리를 가장 많이 쓰는 프로세스를 강제로 죽이는 **"OOM Killer"**가 동작합니다.

### 2-5. 질문 2 — MEMORY_LIMIT을 높이는 것이 근본 해결책인가?

> **아닙니다. 임시방편입니다.**
>
> 우리가 한 조치는 `MEMORY_LIMIT=256 → 512`로 **한계치를 올린 것**뿐입니다.
> 이렇게 하면 더 오래 버티긴 하지만, 누수 자체(메모리를 안 비워주는 코드)는
> 그대로이기 때문에 결국 512MB도 넘게 됩니다.
>
> 비유하자면, 책장이 가득 찼다고 책장을 더 큰 걸로 바꾼 것과 같습니다.
> 진짜 해결책은 **"다 읽은 책은 반납한다"** — 즉, 코드에서 다 쓴 메모리를
> `del`이나 `free()` 등으로 명시적으로 해제하도록 고치는 것입니다.

---

## 3. Case 2 — CPU Spike (CPU 과점유)

### 3-1. 무슨 명령을 실행했나

```bash
python3 agent-leak-sim.py
# 메뉴에서 "2" 입력 → Enter (CPU Spike 프리셋 적용)
```

적용된 설정값:
```
MEMORY_LIMIT        = 9999 MB  (메모리 때문에 먼저 안 죽도록 매우 높게 설정)
CPU_MAX_OCCUPY      = 50 %
MULTI_THREAD_ENABLE = false
```

### 3-2. 실행 결과 (실제 로그)

```
2026-06-09 17:37:50 [INFO] --- Step Info: Mode=UP, CPU Lv=8, Mem=200MB ---
2026-06-09 17:37:50 [INFO] [CPU] Occupy core for 4.0s (Level 8)
2026-06-09 17:37:50 [WARNING] [Watchdog] CPU usage spike detected: 99.7% > 50%
2026-06-09 17:37:50 [CRITICAL] [Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)
>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<
```

### 3-3. 로그 한 줄씩 해석

| 로그 | 의미 |
|---|---|
| `[CPU] Occupy core for 4.0s (Level 8)` | CPU 코어 1개를 4초 동안 계산으로 꽉 채운다는 뜻. Level이 높을수록 점유 시간이 길어짐 |
| `CPU usage spike detected: 99.7% > 50%` | 실제 측정한 CPU 사용률(99.7%)이 허용 한계(50%)를 초과 |
| `INITIATING EMERGENCY ABORT (SIGTERM)` | "SIGTERM" 신호를 보내 프로세스를 정상 종료시키라고 명령 |
| `WATCHDOG: PROCESS TERMINATED` | Watchdog(감시견) 정책에 의해 종료됨을 알리는 메시지 |

### 3-4. 질문 1 — CPU 과점유가 시스템 전체에 미치는 영향은?

> CPU는 여러 프로그램이 **시간을 나눠가며(time-sharing)** 사용하는 자원입니다.
>
> 우리 실습에서 `agent-leak-sim`이 CPU Level 8에서 **4초간 코어를 100% 가까이
> 점유**했습니다. 만약 이 상태가 계속되면, 같은 컴퓨터에서 돌아가는 다른 프로그램들은
> CPU 차례를 기다리느라 응답이 느려집니다.
>
> 예를 들어 이게 웹 서버였다면, 모든 사용자의 요청 처리가 늦어지고
> 결국 "응답 시간 초과(timeout)"가 발생할 수 있습니다.

### 3-5. 질문 2 — Watchdog이 SIGTERM을 보내는 이유는?

> **SIGTERM**은 "강제로 죽이는" 신호가 아니라 **"정상적으로 마무리하고 종료해라"**
> 라는 신호입니다.
>
> 우리 로그에서 `INITIATING EMERGENCY ABORT (SIGTERM)`이 나온 것처럼,
> Watchdog은 프로세스가 CPU를 너무 많이 쓴다고 판단되면 SIGTERM을 보내서
> "파일 닫기, 로그 저장 같은 마무리 작업을 한 뒤 스스로 종료하라"고 요청합니다.
>
> 이와 반대로 **SIGKILL(`kill -9`)**은 마무리 작업 없이 즉시 강제 종료시키는
> 신호로, 데이터 손실 위험이 있어 최후의 수단으로만 사용합니다.

### 3-6. 질문 3 — CPU_MAX_OCCUPY를 높이는 것이 근본 해결책인가?

> Memory와 마찬가지로 **임시방편**입니다.
> 우리가 `CPU_MAX_OCCUPY=50 → 90`으로 올리면 Watchdog이 더 늦게,
> 또는 덜 자주 발동하지만, **CPU를 독점하는 코드 자체**(Level 8~10에서
> 4~5초씩 코어를 꽉 채우는 연산)는 그대로입니다.
>
> 근본 해결책은 그 연산을 여러 작업으로 **잘게 쪼개거나**, 중간중간
> `sleep`을 넣어 다른 프로세스에게 CPU를 양보(yield)하도록 코드를
> 개선하는 것입니다.

---

## 4. Case 3 — Deadlock (교착상태)

### 4-1. 무슨 명령을 실행했나

```bash
python3 agent-leak-sim.py
# 메뉴에서 "3" 입력 → Enter (Deadlock 프리셋 적용)
```

적용된 설정값:
```
MEMORY_LIMIT        = 9999 MB
CPU_MAX_OCCUPY      = 100 %
MULTI_THREAD_ENABLE = true   ← 핵심: 멀티스레드 켜짐
```

### 4-2. 실행 결과 (실제 로그 + 프로세스 확인)

```
2026-06-09 17:45:28 [INFO] [Thread-A] Acquired Lock-1, WAITING for Lock-2...
2026-06-09 17:45:28 [INFO] [Thread-B] Acquired Lock-2, WAITING for Lock-1...
(이후 로그 없음 — 영원히 멈춤)
```

다른 터미널에서 실행한 명령과 결과:
```bash
ps -ef | grep agent-leak-sim
```
```
1267600670 28648 27145   0  5:44PM ttys010   0:55.09 .../Python agent-leak-sim.py
```

### 4-3. 명령어 / 로그 해석

| 명령·로그 | 의미 |
|---|---|
| `ps -ef \| grep agent-leak-sim` | `ps -ef`: 현재 실행 중인 모든 프로세스 목록 출력. `grep`: 그 중 "agent-leak-sim"이 포함된 줄만 골라냄 |
| `28648` | 이 프로세스의 PID (Process ID). **PID가 보인다 = 프로세스가 살아있다** |
| `0:55.09` (TIME) | 이 프로세스가 지금까지 사용한 누적 CPU 시간. **시간이 더 안 늘어난다 = 더 이상 일을 안 하고 있다** |
| `[Thread-A] Acquired Lock-1, WAITING for Lock-2...` | A 스레드가 자물쇠1(Lock-1)은 잡았는데, 자물쇠2(Lock-2)를 기다리는 중 |
| `[Thread-B] Acquired Lock-2, WAITING for Lock-1...` | B 스레드가 자물쇠2(Lock-2)는 잡았는데, 자물쇠1(Lock-1)을 기다리는 중 |

→ A는 B가 가진 것을 기다리고, B는 A가 가진 것을 기다림 → **서로 영원히 대기 = Deadlock**

### 4-4. 질문 1 — Deadlock의 4대 조건이란?

식사하는 철학자 비유: 두 사람이 젓가락을 한 짝씩 들고 서로의 나머지 한 짝을
기다리면, 아무도 밥을 먹을 수 없습니다. 이런 상황은 아래 4가지가 **모두**
충족될 때 발생합니다.

| 조건 | 설명 | 우리 실습에서는 |
|---|---|---|
| 상호 배제 (Mutual Exclusion) | 자원(락)은 한 번에 한 스레드만 사용 가능 | `threading.Lock()` — 한 번에 하나만 획득 가능 |
| 점유 대기 (Hold and Wait) | 자원을 가진 채로 다른 자원을 기다림 | Thread-A가 Lock-1을 쥔 채 Lock-2를 기다림 |
| 비선점 (No Preemption) | 다른 스레드의 자원을 강제로 빼앗을 수 없음 | Thread-B의 Lock-2를 A가 강제로 가져올 수 없음 |
| 순환 대기 (Circular Wait) | A→B→A처럼 순환하며 서로 기다림 | A는 B의 Lock-2를, B는 A의 Lock-1을 기다림 (순환) |

이 중 **하나라도 깨면** Deadlock을 막을 수 있습니다 (예: 항상 Lock-1 →
Lock-2 순서로만 획득하게 강제하면 순환 대기가 사라짐).

### 4-5. 질문 2 — Deadlock 프로세스를 어떻게 식별하나요?

> 핵심 판단 기준은 다음과 같습니다.
>
> ```
> 정상 프로세스: PID 있음 + CPU/MEM 변화 있음 + 로그 출력 중
> Deadlock 상태: PID 있음 + CPU/MEM 변화 없음 + 로그 완전히 멈춤
> ```
>
> 우리 실습에서:
> 1. `ps -ef | grep agent-leak-sim` → **PID 28648 존재** (살아있음)
> 2. TIME 값(`0:55.09`)이 더 이상 증가하지 않음 → **CPU 작업 안 함**
> 3. 로그가 `[Thread-A]`, `[Thread-B]` 줄 이후 더 이상 출력되지 않음 → **무응답**
>
> 세 가지가 모두 맞아떨어지므로 "프로세스는 살아있지만 멈춰버린 Deadlock 상태"라고
> 결론지을 수 있습니다.

### 4-6. 질문 3 — MULTI_THREAD_ENABLE=false가 근본 해결책인가요?

> **아닙니다.** 멀티스레드를 끄면 Deadlock은 안 생기지만,
> 동시에 여러 작업을 처리하던 **성능상의 이점도 함께 사라집니다.**
>
> 진짜 해결책은 두 가지입니다.
> 1. **락 획득 순서 통일**: 모든 스레드가 항상 "Lock-1을 먼저, Lock-2를 나중에"
>    순서로만 획득하도록 코드를 작성 → 순환 대기 자체가 발생할 수 없음
> 2. **타임아웃 설정**: 락을 일정 시간 이상 기다려도 못 얻으면 포기하고
>    재시도하도록 만들기 (`lock.acquire(timeout=...)`)

---

## 5. 리포팅 — 왜 GitHub Issue로 작성했나?

### 실행한 작업

각 케이스마다 아래와 같은 구조의 마크다운 문서를 작성했습니다:

```
## 1. Description (현상 설명)
## 2. Evidence & Logs (증거 자료)
## 3. Root Cause Analysis (원인 분석)
## 4. Workaround & Verification (조치 및 검증)
## 5. 관련 환경변수
```

그리고 git 명령으로 GitHub에 올렸습니다:

```bash
git add 파일명
git commit -m "커밋 메시지"
git push origin main
```

| 명령 | 의미 |
|---|---|
| `git add 파일명` | 이 파일을 "다음 커밋에 포함시킬 목록"에 추가 |
| `git commit -m "메시지"` | 추가된 변경사항을 하나의 "저장 시점(스냅샷)"으로 기록 |
| `git push origin main` | 로컬에 기록된 커밋을 GitHub의 main 브랜치로 업로드 |

이후 GitHub 웹사이트에서 **New Issue**를 눌러 같은 내용을 Issue로 등록했습니다.

### 질문 — GitHub Issue 형태로 리포트를 작성하는 이유는?

> 장애 원인을 혼자만 알고 끝내면, **같은 장애가 나중에 또 발생했을 때
> 처음부터 다시 분석**해야 합니다.
>
> Issue로 남기면:
> 1. **재현 방법 공유** — 다른 사람도 같은 환경변수로 같은 문제를 재현할 수 있음
> 2. **조치 결과 검증** — Before/After 비교가 기록에 남아, "진짜 고쳐졌는지" 누구나 확인 가능
> 3. **나중을 위한 참고자료** — 비슷한 장애가 또 발생하면 과거 Issue를 검색해서
>    빠르게 원인을 추정할 수 있음
>
> 즉, **"내 머릿속의 지식"을 "팀 전체의 자산"으로 바꾸는 작업**입니다.

---

## 6. 전체 흐름 요약 (한 장 정리)

```
┌─────────────────────────────────────────────────────────────┐
│  agent-leak-sim.py 실행 → 케이스 선택(1/2/3)                  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   [Case 1]               [Case 2]               [Case 3]
 Memory Leak            CPU Spike              Deadlock
        │                     │                     │
 25MB씩 계속 증가      CPU Lv 1→10 증가       Lock-1/Lock-2
        │                     │              순환 대기 발생
 256MB 초과 시          Lv8 이상에서             │
 MemoryGuard 발동      실제 CPU 99.7%        로그 멈춤,
        │              > 50% → Watchdog       PID는 생존
 SELF-TERMINATED       PROCESS TERMINATED          │
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                    로그 캡처 → 원인 분석
                    → 설정 조정(Before/After)
                              │
                    GitHub Issue 3건 작성
                    (Description / Evidence /
                     Root Cause / Workaround)
                              │
                       최종 제출
```
