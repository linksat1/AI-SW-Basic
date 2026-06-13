#!/usr/bin/env python3
"""
agent-leak-sim — B1-2 미션용 장애 시뮬레이션 앱

환경변수:
  MEMORY_LIMIT        (default 256)   메모리 상한 (MB)
  CPU_MAX_OCCUPY      (default 50)    CPU 임계치 (%)
  MULTI_THREAD_ENABLE (default true)  멀티스레드 활성화
  AGENT_HOME          (default .)     로그 fallback 경로
"""

import os, sys, time, math, threading, datetime
# os: 환경변수·경로·프로세스 제어 / sys: 프로세스 종료 / time: 대기·시간 측정
# math: CPU 점유용 연산 / threading: Deadlock 재현용 멀티스레드 / datetime: 로그 타임스탬프

# ── 설정 ──────────────────────────────────────────────────────────
# os.environ.get('이름', 기본값) → 환경변수가 있으면 그 값을, 없으면 기본값을 사용
MEMORY_LIMIT        = int(os.environ.get('MEMORY_LIMIT', 256))      # 메모리 누수 한계치(MB) — 도달 시 자가 종료
CPU_MAX_OCCUPY      = int(os.environ.get('CPU_MAX_OCCUPY', 50))     # CPU 사용률 임계치(%) — Watchdog 감시 기준
MULTI_THREAD_ENABLE = os.environ.get('MULTI_THREAD_ENABLE', 'true').lower() == 'true'  # Deadlock 시나리오 on/off
AGENT_HOME          = os.environ.get('AGENT_HOME', '.')             # 시스템 로그 경로를 못 쓸 때 대신 쓸 로컬 폴더

# ── 로그 경로 (sudo 없이 동작) ────────────────────────────────────
_SYS = '/var/log/agent-app'
# 원본 프로그램과 같은 시스템 경로(_SYS)에 쓸 수 있는지 확인.
#  - 쓸 수 있으면(=관리자 권한 있음) 그 경로를 그대로 사용
#  - 쓸 수 없으면(일반 사용자 권한) 현재 폴더 밑 'logs/' 디렉터리에 대신 기록 → sudo 불필요
LOG_DIR  = _SYS if (os.path.isdir(_SYS) and os.access(_SYS, os.W_OK)) \
           else os.path.join(AGENT_HOME, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)   # logs 폴더가 없으면 생성 (있으면 에러 없이 통과)
LOG_FILE = os.path.join(LOG_DIR, 'agent_app.log')


def log(level, msg):
    # 타임스탬프를 붙여 화면(콘솔)과 로그 파일에 동시에 기록
    ts   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{ts} [{level}] {msg}"
    print(line, flush=True)          # flush=True: 버퍼링 없이 즉시 화면에 출력
    try:
        with open(LOG_FILE, 'a') as f:   # 'a' = append, 파일 끝에 이어쓰기
            f.write(line + '\n')
    except OSError:
        pass                          # 로그 파일에 못 써도 프로그램은 계속 진행


# ── 부팅 시퀀스 ───────────────────────────────────────────────────
def boot():
    # 실제 서비스가 켜질 때 거치는 "사전 점검(헬스체크)" 단계를 흉내냄
    print(">>> Starting Agent Boot Sequence...", flush=True)
    steps = [
        ("Checking User Account",           True),
        ("Verifying Environment Variables", MEMORY_LIMIT > 0 and CPU_MAX_OCCUPY > 0),
        ("Checking Required Files",         True),
        ("Checking Port Availability",      True),
        ("Verifying Log Permission",        os.access(LOG_DIR, os.W_OK)),  # 로그 폴더 쓰기 권한 실제 점검
    ]
    for i, (name, ok) in enumerate(steps, 1):
        time.sleep(0.3)                # 0.3초씩 대기 → 실제로 점검하는 것처럼 보이게
        print(f"[{i}/5] {name:<40} {'[OK]' if ok else '[FAIL]'}", flush=True)
        if not ok:
            sys.exit(1)                # 점검 실패 시 즉시 종료 (exit code 1 = 비정상 종료)
    print("-" * 60, flush=True)
    print("All Boot Checks Passed!", flush=True)
    print("Agent READY\n", flush=True)
    log("INFO", f"Agent started — MEMORY_LIMIT={MEMORY_LIMIT}MB "
                f"CPU_MAX_OCCUPY={CPU_MAX_OCCUPY}% "
                f"MULTI_THREAD_ENABLE={MULTI_THREAD_ENABLE}")
    log("INFO", f"Log: {LOG_FILE}")


# ── CPU 시뮬레이션 ────────────────────────────────────────────────
def _burn(seconds):
    # 지정한 시간(seconds) 동안 CPU를 점유하는 "바쁜 대기(busy loop)".
    # sleep은 CPU를 안 쓰고 쉬므로, 일부러 의미 없는 연산(sqrt)을 반복해 CPU 사용률을 끌어올림
    end = time.monotonic() + seconds
    x   = 1.0
    while time.monotonic() < end:
        x = math.sqrt(x + 1.0)


def cpu_step(level):
    # level(1~10)이 높을수록 CPU를 더 오래 점유 → CPU 사용률이 Lv에 비례해 출렁임
    burn_sec = level * 0.5           # Lv=1 → 0.5초, Lv=10 → 5초
    log("INFO", f"[CPU] Occupy core for {burn_sec:.1f}s (Level {level})")

    t0_wall = time.monotonic()                 # 실제 경과 시간(벽시계) 측정 시작
    t0_cpu  = sum(os.times()[:2])    # user + sys CPU 시간 (지금까지 사용한 CPU 시간 합계)
    _burn(burn_sec)
    wall   = max(time.monotonic() - t0_wall, 0.001)
    actual = (sum(os.times()[:2]) - t0_cpu) / wall * 100   # 실제 CPU 사용률(%) = CPU시간 / 경과시간

    # Lv>=8 (고부하 구간)에서만 Watchdog 체크
    # → "CPU 급등 감지 → 비상 종료(SIGTERM)" 흐름을 재현
    if level >= 8 and actual > CPU_MAX_OCCUPY:
        log("WARNING",  f"[Watchdog] CPU usage spike detected: {actual:.1f}% > {CPU_MAX_OCCUPY}%")
        log("CRITICAL", "[Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)")
        print(">>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<", flush=True)
        sys.exit(0)                  # 정상 종료(exit code 0)로 프로세스 끝냄


# ── 메모리 시뮬레이션 (누수: DOWN에서 해제 안 함) ──────────────────
_pool   = []   # 해제되지 않는 메모리 풀 — 계속 추가만 하고 절대 비우지 않음 (메모리 누수 흉내)
_mem_mb = 0


def mem_increase():
    global _mem_mb
    _pool.append(bytearray(25 * 1024 * 1024))   # 실제 25 MB 바이트 배열을 만들어 _pool에 추가 (진짜 메모리 점유)
    _mem_mb += 25
    log("INFO", f"[Memory] Increasing... (+25 MB) Total: {_mem_mb} MB")
    if _mem_mb >= MEMORY_LIMIT:
        # MemoryGuard: 메모리 사용량이 한계를 넘으면, 시스템 전체가 죽기 전에 이 프로세스가 스스로 종료
        log("CRITICAL", f"[MemoryGuard] Memory limit exceeded ({_mem_mb}MB >= {MEMORY_LIMIT}MB)")
        log("CRITICAL", f"[MemoryGuard] Self-terminating process {os.getpid()} to prevent system instability.")
        print(">>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<", flush=True)
        sys.exit(0)


# ── Deadlock 시뮬레이션 ───────────────────────────────────────────
# 두 잠금(Lock)을 서로 "반대 순서"로 잡으려다 영원히 멈추는 고전적인 교착상태(Deadlock) 패턴
_lock1  = threading.Lock()
_lock2  = threading.Lock()
_ready1 = threading.Event()   # Thread-A가 Lock-1 보유 신호
_ready2 = threading.Event()   # Thread-B가 Lock-2 보유 신호


def _thread_a():
    _lock1.acquire()           # ① Lock-1을 먼저 잡음
    log("INFO", "[Thread-A] Acquired Lock-1, WAITING for Lock-2...")
    _ready1.set()              # "Lock-1 확보" 알림 (Thread-B에게 신호)
    _ready2.wait()             # ② Thread-B가 Lock-2 확보할 때까지 대기
    _lock2.acquire()           # ③ Lock-2를 잡으려 함 → 이미 Thread-B가 보유 중 → 영원히 블록


def _thread_b():
    _lock2.acquire()           # ① Lock-2를 먼저 잡음 (A와 반대 순서!)
    log("INFO", "[Thread-B] Acquired Lock-2, WAITING for Lock-1...")
    _ready2.set()              # "Lock-2 확보" 알림 (Thread-A에게 신호)
    _ready1.wait()             # ② Thread-A가 Lock-1 확보할 때까지 대기
    _lock1.acquire()           # ③ Lock-1을 잡으려 함 → 이미 Thread-A가 보유 중 → 영원히 블록
    # 결과: A는 Lock-2를, B는 Lock-1을 서로 기다리며 둘 다 영원히 멈춤 = Deadlock


def trigger_deadlock():
    log("INFO", "[Scheduler] Starting multi-thread task...")
    ta = threading.Thread(target=_thread_a, daemon=True)
    tb = threading.Thread(target=_thread_b, daemon=True)
    ta.start()
    tb.start()
    ta.join()                  # ta가 끝나길 기다리는데 ta는 영원히 안 끝남 → 메인 스레드도 블록 → 로그 완전 정지


# ── 대화형 케이스 선택 ───────────────────────────────────────────
def interactive_setup():
    presets = {
        '1': (256,  100, False),   # Case1 메모리 누수: 한계 256MB → 곧 도달해 자가 종료
        '2': (9999,  50, False),   # Case2 CPU 과점유: 메모리 한계는 거의 무제한, CPU 임계치 50%
        '3': (9999, 100, True),    # Case3 Deadlock: 멀티스레드 활성화 → 첫 RAMP DOWN 후 교착 발생
    }
    labels = {
        '1': 'Memory Leak  (메모리 누수)',
        '2': 'CPU Spike    (CPU 과점유)',
        '3': 'Deadlock     (교착상태)',
    }

    print()
    print("=" * 44)
    print("  agent-leak-sim — B1-2 장애 시뮬레이터")
    print("=" * 44)
    print()
    print("실행할 케이스를 선택하세요:")
    for k, v in labels.items():
        print(f"  [{k}] {v}")
    print()

    while True:
        choice = input("선택 (1-3): ").strip()
        if choice in presets:
            break
        print("  → 1, 2, 3 중 하나를 입력하세요.")

    mem, cpu, mt = presets[choice]

    print()
    print("── 설정값 " + "─" * 34)
    print(f"  MEMORY_LIMIT        = {mem} MB")
    print(f"  CPU_MAX_OCCUPY      = {cpu} %")
    print(f"  MULTI_THREAD_ENABLE = {str(mt).lower()}")
    print("─" * 44)
    print()

    ans = input("이 설정으로 실행합니까? (Enter=예 / n=직접입력): ").strip().lower()
    if ans == 'n':
        raw = input(f"  MEMORY_LIMIT [{mem}]: ").strip()
        if raw:
            mem = int(raw)
        raw = input(f"  CPU_MAX_OCCUPY [{cpu}]: ").strip()
        if raw:
            cpu = int(raw)
        raw = input(f"  MULTI_THREAD_ENABLE [{str(mt).lower()}] (true/false): ").strip().lower()
        if raw in ('true', 'false'):
            mt = raw == 'true'

    print()
    return mem, cpu, mt


# ── 메인 루프 ────────────────────────────────────────────────────
def main():
    global MEMORY_LIMIT, CPU_MAX_OCCUPY, MULTI_THREAD_ENABLE
    MEMORY_LIMIT, CPU_MAX_OCCUPY, MULTI_THREAD_ENABLE = interactive_setup()
    boot()

    mode       = "UP"      # UP: CPU 레벨 1→10 상승 / DOWN: 10→1 하강
    cpu_level  = 1
    down_count = 0         # DOWN 모드를 몇 번 완료했는지 (Deadlock 발생 조건에 사용)

    while True:
        log("INFO", f"--- Step Info: Mode={mode}, CPU Lv={cpu_level}, Mem={_mem_mb}MB ---")

        if mode == "UP":
            mem_increase()     # UP 모드에서만 메모리 +25MB (MEMORY_LIMIT 도달 시 자가 종료)
        # DOWN 모드: 메모리 해제 없음 (누수 재현) → 메모리는 절대 줄지 않음

        cpu_step(cpu_level)    # CPU_MAX_OCCUPY 초과 시 종료 (Lv>=8에서만 체크)

        time.sleep(0.5)        # 다음 스텝까지 0.5초 대기

        if mode == "UP":
            if cpu_level < 10:
                cpu_level += 1
            else:
                log("INFO", ">>> TOP REACHED. Switching to RAMP DOWN. ▼ <<<")
                mode = "DOWN"          # 레벨 10에 도달하면 하강 시작
        else:
            if cpu_level > 1:
                cpu_level -= 1
            else:
                log("INFO", ">>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<")
                mode       = "UP"
                down_count += 1
                if MULTI_THREAD_ENABLE and down_count >= 1:
                    trigger_deadlock()   # 첫 RAMP DOWN 완료 시 Deadlock 발생 → 반환 없음(로그 영구 정지, 프로세스는 살아있음)


if __name__ == '__main__':
    main()
