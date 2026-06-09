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

# ── 설정 ──────────────────────────────────────────────────────────
MEMORY_LIMIT        = int(os.environ.get('MEMORY_LIMIT', 256))
CPU_MAX_OCCUPY      = int(os.environ.get('CPU_MAX_OCCUPY', 50))
MULTI_THREAD_ENABLE = os.environ.get('MULTI_THREAD_ENABLE', 'true').lower() == 'true'
AGENT_HOME          = os.environ.get('AGENT_HOME', '.')

# ── 로그 경로 (sudo 없이 동작) ────────────────────────────────────
_SYS = '/var/log/agent-app'
LOG_DIR  = _SYS if (os.path.isdir(_SYS) and os.access(_SYS, os.W_OK)) \
           else os.path.join(AGENT_HOME, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'agent_app.log')


def log(level, msg):
    ts   = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{ts} [{level}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except OSError:
        pass


# ── 부팅 시퀀스 ───────────────────────────────────────────────────
def boot():
    print(">>> Starting Agent Boot Sequence...", flush=True)
    steps = [
        ("Checking User Account",           True),
        ("Verifying Environment Variables", MEMORY_LIMIT > 0 and CPU_MAX_OCCUPY > 0),
        ("Checking Required Files",         True),
        ("Checking Port Availability",      True),
        ("Verifying Log Permission",        os.access(LOG_DIR, os.W_OK)),
    ]
    for i, (name, ok) in enumerate(steps, 1):
        time.sleep(0.3)
        print(f"[{i}/5] {name:<40} {'[OK]' if ok else '[FAIL]'}", flush=True)
        if not ok:
            sys.exit(1)
    print("-" * 60, flush=True)
    print("All Boot Checks Passed!", flush=True)
    print("Agent READY\n", flush=True)
    log("INFO", f"Agent started — MEMORY_LIMIT={MEMORY_LIMIT}MB "
                f"CPU_MAX_OCCUPY={CPU_MAX_OCCUPY}% "
                f"MULTI_THREAD_ENABLE={MULTI_THREAD_ENABLE}")
    log("INFO", f"Log: {LOG_FILE}")


# ── CPU 시뮬레이션 ────────────────────────────────────────────────
def _burn(seconds):
    end = time.monotonic() + seconds
    x   = 1.0
    while time.monotonic() < end:
        x = math.sqrt(x + 1.0)


def cpu_step(level):
    burn_sec = level * 0.5           # Lv=1 → 0.5초, Lv=10 → 5초
    log("INFO", f"[CPU] Occupy core for {burn_sec:.1f}s (Level {level})")

    t0_wall = time.monotonic()
    t0_cpu  = sum(os.times()[:2])    # user + sys CPU 시간
    _burn(burn_sec)
    wall   = max(time.monotonic() - t0_wall, 0.001)
    actual = (sum(os.times()[:2]) - t0_cpu) / wall * 100

    # Lv>=8 (고부하 구간)에서만 Watchdog 체크
    if level >= 8 and actual > CPU_MAX_OCCUPY:
        log("WARNING",  f"[Watchdog] CPU usage spike detected: {actual:.1f}% > {CPU_MAX_OCCUPY}%")
        log("CRITICAL", "[Watchdog] INITIATING EMERGENCY ABORT (SIGTERM)")
        print(">>> [SYSTEM] WATCHDOG: PROCESS TERMINATED <<<", flush=True)
        sys.exit(0)


# ── 메모리 시뮬레이션 (누수: DOWN에서 해제 안 함) ──────────────────
_pool   = []   # 해제되지 않는 메모리 풀
_mem_mb = 0


def mem_increase():
    global _mem_mb
    _pool.append(bytearray(25 * 1024 * 1024))   # 실제 25 MB 할당
    _mem_mb += 25
    log("INFO", f"[Memory] Increasing... (+25 MB) Total: {_mem_mb} MB")
    if _mem_mb >= MEMORY_LIMIT:
        log("CRITICAL", f"[MemoryGuard] Memory limit exceeded ({_mem_mb}MB >= {MEMORY_LIMIT}MB)")
        log("CRITICAL", f"[MemoryGuard] Self-terminating process {os.getpid()} to prevent system instability.")
        print(">>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<", flush=True)
        sys.exit(0)


# ── Deadlock 시뮬레이션 ───────────────────────────────────────────
_lock1  = threading.Lock()
_lock2  = threading.Lock()
_ready1 = threading.Event()   # Thread-A가 Lock-1 보유 신호
_ready2 = threading.Event()   # Thread-B가 Lock-2 보유 신호


def _thread_a():
    _lock1.acquire()
    log("INFO", "[Thread-A] Acquired Lock-1, WAITING for Lock-2...")
    _ready1.set()              # "Lock-1 확보" 알림
    _ready2.wait()             # Thread-B가 Lock-2 확보할 때까지 대기
    _lock2.acquire()           # Thread-B가 보유 중 → 영원히 블록


def _thread_b():
    _lock2.acquire()
    log("INFO", "[Thread-B] Acquired Lock-2, WAITING for Lock-1...")
    _ready2.set()              # "Lock-2 확보" 알림
    _ready1.wait()             # Thread-A가 Lock-1 확보할 때까지 대기
    _lock1.acquire()           # Thread-A가 보유 중 → 영원히 블록


def trigger_deadlock():
    log("INFO", "[Scheduler] Starting multi-thread task...")
    ta = threading.Thread(target=_thread_a, daemon=True)
    tb = threading.Thread(target=_thread_b, daemon=True)
    ta.start()
    tb.start()
    ta.join()                  # 메인 스레드도 블록 → 로그 완전 정지


# ── 대화형 케이스 선택 ───────────────────────────────────────────
def interactive_setup():
    presets = {
        '1': (256,  100, False),
        '2': (9999,  50, False),
        '3': (9999, 100, True),
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

    mode       = "UP"
    cpu_level  = 1
    down_count = 0

    while True:
        log("INFO", f"--- Step Info: Mode={mode}, CPU Lv={cpu_level}, Mem={_mem_mb}MB ---")

        if mode == "UP":
            mem_increase()     # MEMORY_LIMIT 도달 시 종료
        # DOWN 모드: 메모리 해제 없음 (누수 재현)

        cpu_step(cpu_level)    # CPU_MAX_OCCUPY 초과 시 종료

        time.sleep(0.5)

        if mode == "UP":
            if cpu_level < 10:
                cpu_level += 1
            else:
                log("INFO", ">>> TOP REACHED. Switching to RAMP DOWN. ▼ <<<")
                mode = "DOWN"
        else:
            if cpu_level > 1:
                cpu_level -= 1
            else:
                log("INFO", ">>> BOTTOM REACHED (Idle). Switching to RAMP UP. ▲ <<<")
                mode       = "UP"
                down_count += 1
                if MULTI_THREAD_ENABLE and down_count >= 1:
                    trigger_deadlock()   # 반환 없음 → 프로세스는 살아있으나 로그 정지


if __name__ == '__main__':
    main()
