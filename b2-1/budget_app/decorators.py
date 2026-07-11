"""공통 관심사(예외 처리 / 실행 로그 + 시간 측정)를 분리한 데코레이터 모음."""
from __future__ import annotations

import functools
import sys
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from budget_app.errors import AppError

LOG_FILE = Path("budget_app.log")


def handle_errors(func: Callable[..., int | None]) -> Callable[..., int]:
    """CLI 명령 함수를 감싸서 예외를 '원인 + 힌트' 메시지로 바꾸고,
    정상 종료는 0, 오류 종료는 0이 아닌 값을 반환하도록 한다.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> int:
        try:
            result = func(*args, **kwargs)
            return 0 if result is None else int(result)
        except AppError as e:
            print(f"[오류] {e.message}", file=sys.stderr)
            if e.hint:
                print(f"[힌트] {e.hint}", file=sys.stderr)
            return 1
        except Exception as e:  # 예상 못한 오류도 스택트레이스 없이 처리
            print(f"[오류] 처리 중 문제가 발생했습니다: {e}", file=sys.stderr)
            print("[힌트] 입력값을 확인하거나, 문제가 반복되면 관리자에게 문의하세요.", file=sys.stderr)
            return 1

    return wrapper


def log_execution(func: Callable) -> Callable:
    """명령 실행 시작/종료와 걸린 시간을 budget_app.log 파일에 기록한다."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "OK"
        try:
            return func(*args, **kwargs)
        except Exception:
            status = "ERROR"
            raise
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(
                    f"[{timestamp}] {func.__name__} status={status} "
                    f"elapsed={elapsed_ms:.1f}ms\n"
                )

    return wrapper
