"""Mini Git에서 발생하는 '예상된' 오류들.

과제 명세의 표준 에러 메시지(Invalid args / Unknown branch: <name> /
Unknown commit: <hash>)를 각각의 예외 클래스로 표현한다. cli.py가 이 예외들을
잡아서 화면에 그대로 출력한다.
"""


class MiniGitError(Exception):
    """Mini Git의 모든 '예상된' 오류의 기반 클래스."""


class InvalidArgsError(MiniGitError):
    def __init__(self):
        super().__init__("Invalid args")


class UnknownBranchError(MiniGitError):
    def __init__(self, name: str):
        super().__init__("Unknown branch: {}".format(name))


class UnknownCommitError(MiniGitError):
    def __init__(self, commit_hash: str):
        super().__init__("Unknown commit: {}".format(commit_hash))


class NotInitializedError(MiniGitError):
    """과제 명세의 3개 표준 에러 외에, INIT 이전에 다른 명령을 쓴 경우를 위해
    추가한 안내용 에러. ("최소 에러 메시지를 표준화한다"는 최소 요구사항 위에
    사용성을 위해 얹은 확장)."""

    def __init__(self):
        super().__init__("Repository not initialized. Run INIT first.")
