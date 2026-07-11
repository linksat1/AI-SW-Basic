"""애플리케이션에서 발생하는 '예상된' 오류를 표현하는 예외."""
from __future__ import annotations


class AppError(Exception):
    """사용자 입력 오류, 존재하지 않는 데이터 등 예상 가능한 오류.

    스택트레이스 대신 원인(message)과 해결 힌트(hint)만 사용자에게 보여준다.
    """

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint
