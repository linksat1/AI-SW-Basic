"""Mini Redis REPL(Read-Eval-Print Loop) CLI.

사용자가 `mini-redis> ` 프롬프트에 명령을 입력하면
  1) 한 줄을 토큰으로 분리하고 (parsing)
  2) store.py의 MiniRedisStore 메서드를 호출해 실행하고 (execute)
  3) Redis 스타일 문자열(OK / (nil) / (integer) N / (error) ...)로
     결과를 출력한다 (print)
과정을 exit/quit을 입력할 때까지 반복한다.

store.py는 "무엇을 저장할지"만 알고, "사용자가 어떤 형식으로 입력했는지"나
"화면에 어떻게 보여줄지"는 전혀 모른다. 이 파일이 그 사이의 번역을 담당한다.
"""

import shlex

from mini_redis.store import MiniRedisStore, OOMError

PROMPT = "mini-redis> "


# ======================================================================
# Redis 스타일 출력 포맷터
# ======================================================================

def fmt_ok() -> str:
    return "OK"


def fmt_nil() -> str:
    return "(nil)"


def fmt_integer(n: int) -> str:
    return "(integer) {}".format(n)


def fmt_bulk(s: str) -> str:
    return '"{}"'.format(s)


def fmt_error(msg: str) -> str:
    return "(error) {}".format(msg)


def fmt_array(items) -> str:
    if not items:
        return "(empty array)"
    lines = []
    for i, item in enumerate(items, start=1):
        lines.append('{}. "{}"'.format(i, item))
    return "\n".join(lines)


# ======================================================================
# 표준 에러 메시지 (과제 명세의 "에러 처리 표준"과 문구를 동일하게 맞춘다)
# ======================================================================

def err_unknown_command(cmd: str) -> str:
    return fmt_error("ERR unknown command '{}'".format(cmd))


def err_wrong_args(cmd: str) -> str:
    return fmt_error("ERR wrong number of arguments for '{}' command".format(cmd))


def err_not_integer() -> str:
    return fmt_error("ERR value is not an integer or out of range")


def err_oom() -> str:
    return fmt_error("OOM command not allowed when used_memory > 'maxmemory'")


def _parse_int(token: str):
    """정수 파싱. 성공하면 int, 실패하면 None을 반환한다."""
    try:
        return int(token)
    except (TypeError, ValueError):
        return None


# ======================================================================
# 명령어별 핸들러
# 각 핸들러는 (store, args) -> 출력할 문자열 시그니처를 갖는다.
# ======================================================================

def _cmd_set(store: MiniRedisStore, args):
    if len(args) != 2:
        return err_wrong_args("SET")
    key, value = args
    try:
        store.set(key, value)
    except OOMError:
        return err_oom()
    return fmt_ok()


def _cmd_get(store: MiniRedisStore, args):
    if len(args) != 1:
        return err_wrong_args("GET")
    value = store.get(args[0])
    if value is None:
        return fmt_nil()
    return fmt_bulk(value)


def _cmd_del(store: MiniRedisStore, args):
    if len(args) != 1:
        return err_wrong_args("DEL")
    return fmt_integer(1 if store.delete(args[0]) else 0)


def _cmd_exists(store: MiniRedisStore, args):
    if len(args) != 1:
        return err_wrong_args("EXISTS")
    return fmt_integer(1 if store.exists(args[0]) else 0)


def _cmd_dbsize(store: MiniRedisStore, args):
    if len(args) != 0:
        return err_wrong_args("DBSIZE")
    return fmt_integer(store.dbsize())


def _cmd_keys(store: MiniRedisStore, args):
    if len(args) != 0:
        return err_wrong_args("KEYS")
    return fmt_array(store.keys())


def _cmd_config(store: MiniRedisStore, args):
    # 지원 형식: CONFIG SET maxmemory <bytes>
    if len(args) != 3 or args[0].upper() != "SET" or args[1].lower() != "maxmemory":
        return err_wrong_args("CONFIG")
    bytes_limit = _parse_int(args[2])
    if bytes_limit is None or bytes_limit < 0:
        return err_not_integer()
    store.config_set_maxmemory(bytes_limit)
    return fmt_ok()


def _cmd_info(store: MiniRedisStore, args):
    # 지원 형식: INFO memory
    if len(args) != 1 or args[0].lower() != "memory":
        return err_wrong_args("INFO")
    info = store.info_memory()
    return "used_memory:{}\nmaxmemory:{}\nevicted_keys:{}".format(
        info.used_memory, info.maxmemory, info.evicted_keys
    )


def _cmd_expire(store: MiniRedisStore, args):
    if len(args) != 2:
        return err_wrong_args("EXPIRE")
    seconds = _parse_int(args[1])
    if seconds is None:
        return err_not_integer()
    return fmt_integer(1 if store.expire(args[0], seconds) else 0)


def _cmd_ttl(store: MiniRedisStore, args):
    if len(args) != 1:
        return err_wrong_args("TTL")
    return fmt_integer(store.ttl(args[0]))


def dispatch(store: MiniRedisStore, raw_line: str) -> str:
    """한 줄 입력을 파싱해 실행하고, 출력할 문자열을 반환한다.

    명령어 이름 -> 핸들러 대응을 dict(테이블)로 만들지 않고 if/elif
    사슬로 직접 분기한다(과제 제약: dict 사용 금지를 CLI 라우팅에도
    일관되게 지킨다).
    """
    try:
        tokens = shlex.split(raw_line)
    except ValueError:
        # 예: 큰따옴표가 짝이 안 맞는 경우
        return fmt_error("ERR unbalanced quotes in input")

    if not tokens:
        return ""

    cmd_raw = tokens[0]
    cmd = cmd_raw.upper()
    args = tokens[1:]

    if cmd == "SET":
        return _cmd_set(store, args)
    elif cmd == "GET":
        return _cmd_get(store, args)
    elif cmd == "DEL":
        return _cmd_del(store, args)
    elif cmd == "EXISTS":
        return _cmd_exists(store, args)
    elif cmd == "DBSIZE":
        return _cmd_dbsize(store, args)
    elif cmd == "KEYS":
        return _cmd_keys(store, args)
    elif cmd == "CONFIG":
        return _cmd_config(store, args)
    elif cmd == "INFO":
        return _cmd_info(store, args)
    elif cmd == "EXPIRE":
        return _cmd_expire(store, args)
    elif cmd == "TTL":
        return _cmd_ttl(store, args)
    else:
        return err_unknown_command(cmd_raw)


def run() -> None:
    """REPL 진입점. exit 또는 quit을 입력할 때까지 명령을 계속 받는다."""
    store = MiniRedisStore()
    print("Mini Redis CLI — 종료하려면 exit 또는 quit을 입력하세요.")
    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            print()
            break
        stripped = line.strip()
        if stripped.lower() in ("exit", "quit"):
            break
        if not stripped:
            continue
        result = dispatch(store, stripped)
        if result:
            print(result)
