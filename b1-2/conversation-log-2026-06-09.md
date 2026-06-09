# 대화 로그 — B1-2 미션 세션 (2026-06-09)

> **참고:** 이전 세션(컨텍스트 압축 전)의 대화는 요약본 기반으로 재구성되었습니다.
> 이번 세션(agent-leak-sim.py 개발 이후)은 실제 대화 내용을 기반으로 작성되었습니다.

---

## 이전 세션 요약 (재구성)

**사용자:** github와 연결해줘요

**Claude:** SSH 키를 생성하고 GitHub에 등록하는 방법을 안내합니다...
(ED25519 키 생성 → GitHub 공개키 등록 → SSH 연결 테스트)

**사용자:** 다른 이메일 주소로 깃허브에 접속되어 있으며 연결하고 싶은 레포는 다음과 같습니다. https://github.com/linksat1/AI-SW-Basic

**사용자:** pagchuseon@gmail.com

**Claude:** linksat1 계정으로 SSH 키를 생성하고 GitHub에 연결합니다...

---

### B1-2 미션 환경 설정

**사용자:** vm list를 보는 명령어는?

**Claude:** `orb list` 명령어로 OrbStack VM 목록을 확인할 수 있습니다.

**사용자:** (orb list 결과 공유 — b1-2 VM 확인)

**Claude:** b1-2 VM에 접속하려면: `orb shell -m b1-2`

---

### B1-1 환경 복구 및 agent-leak-app 실행

**Claude:** B1-1 setup.sh를 실행하여 환경을 복구합니다:
```bash
chmod +x 'b1-1 setup.sh'
sudo bash 'b1-1 setup.sh'
```

**사용자:** chmod +x 'b1-1 setup.sh' / sudo bash 'b1-1 setup.sh' 해석해 주세요

**Claude:**
- `chmod +x`: 파일에 실행 권한을 부여합니다. `+x`는 "execute 권한 추가"
- `sudo bash`: 관리자 권한으로 bash 쉘을 통해 스크립트를 실행합니다

---

### Case 1: Memory Leak 관찰

**사용자:** 네 메모리가 증가하고 있습니다. 어디까지 증가하나요?

**Claude:** MEMORY_LIMIT=256MB 설정 기준으로 275MB까지 증가 후 MemoryGuard가 발동하여 앱이 자동 종료됩니다. 25MB씩 증가하므로 약 50초 소요됩니다.

**사용자:** 메모리가 다시 떨어쪘어요

**Claude:** DOWN 모드로 전환된 것입니다. DOWN 모드에서는 메모리가 감소하지만 완전히 해제되지 않는 것이 "메모리 누수"의 특징입니다.

---

### Case 2: CPU Spike 관찰

**사용자:** 케이스 2: CPU Spike도 시간이 오래 걸리네요... 오늘도 pc켜놓고 집에 갔다와야 하나요?

**Claude:** CPU Spike는 약 1분 42초 주기로 Lv=10이 반복됩니다. 충분한 증거가 수집되면 바로 보고서를 작성할 수 있습니다. 현재 로그로도 충분합니다.

**사용자:** 네 (보고서 작성 진행 동의)

**사용자:** 완료하였습니다 (Case 1 GitHub Issue 생성 완료)

---

## 이번 세션 대화 (2026-06-09 오후)

---

**사용자:** @AI-SW-Basic/b1-2/Mission.md 미션에서 요구하는 과제 수행을 위해, 직접 CPU, Memory, Deadlock(multi-thread 여부) 이 세 가지 옵션을 조정할 수 있는 앱을 만들어줘. 가능하다면 쉘 스크립트나 파이썬 프로그램으로. 부가 기능 없이 최소한의 기능만 탑재해서, 간단하게. 참고로, 현재 내 PC환경은 학습용이라서, 관리자 권한(sudo 등)이 막혀 있어. 구현과 테스트에 참고해줘.

**Claude:** Mission.md를 검토하고 계획을 수립합니다.

다음과 같이 `agent-leak-sim.py` Python 스크립트를 만들겠습니다:
- 환경변수: MEMORY_LIMIT, CPU_MAX_OCCUPY, MULTI_THREAD_ENABLE
- 로그 경로: `/var/log/agent-app/` (VM) 또는 `./logs/` (macOS fallback, sudo 불필요)
- Memory Leak: `bytearray`로 실제 25MB 할당
- CPU Spike: `math.sqrt` busy-loop으로 실제 CPU 사용
- Deadlock: `threading.Lock` 순환 대기
- stdlib만 사용 (외부 패키지 없음)

(계획 승인 후 구현)

`/Users/cspag5955/Documents/AI-SW-Basic/b1-2/agent-leak-sim.py` 생성 완료.

테스트 결과:
```
# Case 1 (MEMORY_LIMIT=50)
>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<  ✅

# Case 2 (CPU_MAX_OCCUPY=30)
>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<  ✅

# Case 3 (Deadlock 검증)
[Thread-A] alive=True, [Thread-B] alive=True → Deadlock 발생: True  ✅
```

---

**사용자:** 프로그램이 의도대로 옵션을 건드릴 수 있게 잘 작성된 것 같아요. 그런데, 실행시키는 방법이 너무 번거롭습니다. 대화형으로 간단히 제가 답변만 하면 그 설정대로 실행될 수 있도록 리팩토링 해주세요.

**Claude:** `interactive_setup()` 함수를 추가하여 실행 시 케이스를 대화형으로 선택하도록 리팩토링합니다.

케이스 선택 메뉴:
```
============================================
  agent-leak-sim — B1-2 장애 시뮬레이터
============================================

실행할 케이스를 선택하세요:
  [1] Memory Leak  (메모리 누수)
  [2] CPU Spike    (CPU 과점유)
  [3] Deadlock     (교착상태)

선택 (1-3):
```

---

**사용자:** python3 agent-leak.py
`/Library/Developer/CommandLineTools/usr/bin/python3: can't open file '...agent-leak.py': [Errno 2] No such file or directory`

**Claude:** 파일 이름이 다릅니다. `agent-leak-sim.py` 입니다:
```bash
python3 agent-leak-sim.py
```

**사용자:** python3 agent-sim.py
`can't open file '...agent-sim.py': No such file or directory`

**Claude:** 정확한 파일 이름은 `agent-leak-sim.py` 입니다:
```bash
python3 agent-leak-sim.py
```

---

**사용자:** 구동이 됩니다. 오래 기다려야 하나요?
```
2026-06-09 17:41:46 [INFO] --- Step Info: Mode=DOWN, CPU Lv=10, Mem=250MB ---
```

**Claude:** 케이스 1 실행 중이시군요. 지금 DOWN 모드(Lv=10)에서 내려가는 중입니다.
**약 35초 후** OOM으로 자동 종료됩니다.
- DOWN: Lv=10 → Lv=1 까지 내려가는 데 ~32초
- 그 다음 UP 첫 스텝에서 250MB + 25MB = **275MB ≥ 256MB** → 종료

---

**사용자:** 메세지가 나왔습니다.

**Claude:** Case 1 완료입니다. 이제 Case 2 (CPU Spike)를 실행하려면:
```bash
python3 agent-leak-sim.py
```
실행 후 **`2`** 선택 → Enter. Case 2는 UP 모드에서 Lv=8 도달 시 (~20초) 자동 종료됩니다.

---

**사용자:** `>>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<`

**Claude:** Case 2도 완료입니다. 이제 Case 3 (Deadlock)을 실행합니다.
**`3`** 선택 → Enter.
Case 3는 종료되지 않고 로그가 멈추는 것이 정상입니다. **약 60초 후** 아래 두 줄이 출력되고 그 이후 로그가 완전히 멈춥니다:
```
[Thread-A] Acquired Lock-1, WAITING for Lock-2...
[Thread-B] Acquired Lock-2, WAITING for Lock-1...
```

다른 터미널에서: `ps -ef | grep agent-leak-sim`

---

**사용자:**
```
2026-06-09 17:45:28 [INFO] [Thread-A] Acquired Lock-1, WAITING for Lock-2...
2026-06-09 17:45:28 [INFO] [Thread-B] Acquired Lock-2, WAITING for Lock-1...
```

**Claude:** Deadlock 발생 확인입니다. 이제 로그가 완전히 멈춰있을 겁니다.
다른 터미널에서 프로세스가 살아있는지 확인하세요: `ps -ef | grep agent-leak-sim`

---

**사용자:**
```
1267600670 28648 27145   0  5:44PM ttys010    0:55.09 /Library/.../Python agent-leak-sim.py
```

**Claude:** 완벽합니다. Deadlock 증명 완료입니다.
- **PID 28648** — 프로세스 살아있음
- **CPU 시간 0:55.09** — 더 이상 증가 없음 (스레드 모두 대기 중)
- **로그 멈춤** — Thread-A/B 이후 출력 없음

이제 `Ctrl+C` 로 종료하세요.

3가지 케이스 모두 완료:

| 케이스 | 결과 |
|--------|------|
| Case 1: Memory Leak | `SELF-TERMINATED (Memory Limit Exceeded)` ✅ |
| Case 2: CPU Spike | `WATCHDOG: PROCESS TERMINATED` ✅ |
| Case 3: Deadlock | PID 살아있음 + 로그 멈춤 ✅ |

---

**사용자:** 예. (보고서 작성 및 GitHub 푸시 요청)

**Claude:** Case 3 보고서 `report-case3-deadlock.md` 작성 후 GitHub 푸시 완료.

Case 2, 3 GitHub Issue를 https://github.com/linksat1/AI-SW-Basic/issues 에서 생성해주세요.

---

**사용자:** 수고하였습니다. 이 대화내용도 파일로 만들어서 저장하고 github로 푸쉬해줘요

**Claude:** `session-log-2026-06-09.md` (작업 결과 요약) 작성 후 GitHub 푸시 완료.

---

**사용자:** (GitHub Issues 스크린샷) 이슈가 두개만 있나요?

**Claude:** 화면이 "Created by me" 필터라서 2개만 보이는 것입니다. Case 1 Issue는 상단 탭에 열려 있습니다. https://github.com/linksat1/AI-SW-Basic/issues 에서 3개 모두 확인 가능합니다.

---

**사용자:** 이 대화창도 저장되었나요?

**Claude:** 아니요, 대화 내용 자체는 저장되지 않았습니다. 저장된 것은 작업 결과 요약인 session-log 파일입니다. 실제 대화 원문을 저장하려면 복사하여 파일로 저장하는 방법이 있습니다.

---

**사용자:** 네. 만들어 주세요

**Claude:** 이 파일(`conversation-log-2026-06-09.md`)을 작성하였습니다.

---

## 이번 세션에서 생성된 파일

| 파일 | 설명 |
|------|------|
| `b1-2/agent-leak-sim.py` | 장애 시뮬레이터 Python 앱 |
| `b1-2/report-case3-deadlock.md` | Case 3 Deadlock 보고서 |
| `b1-2/session-log-2026-06-09.md` | 작업 결과 요약 |
| `b1-2/conversation-log-2026-06-09.md` | 이 대화 로그 |

## GitHub Issues

| 번호 | 제목 |
|------|------|
| #1 | [Bug] 메모리 누수로 인한 MemoryGuard 보호 정책 강제 종료 |
| #2 | [Bug] CPU 과점유로 인한 Watchdog 긴급 종료 |
| #3 | [Bug] 멀티스레드 환경에서 교착상태(Deadlock) 발생으로 프로세스 무응답 |
