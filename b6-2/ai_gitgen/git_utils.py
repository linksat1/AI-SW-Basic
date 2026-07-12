"""git status/diff 수집 유틸리티. subprocess만 사용하며 shell=True는 쓰지 않는다."""

import subprocess

from .errors import AiGitGenError, NoChangesError, NotAGitRepoError

# 빈 트리의 git 고정 해시. 초기 커밋 하나뿐인 저장소에서 HEAD~1이 없을 때
# "저장소 시작 시점"을 나타내는 비교 대상으로 사용한다.
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def _run_git(args: list, allow_fail: bool = False):
    """git 명령을 실행한다. allow_fail=True면 실패 시 (None, stderr)를 반환한다."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise NotAGitRepoError() from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if allow_fail:
            return None, stderr
        if "not a git repository" in stderr.lower():
            raise NotAGitRepoError()
        raise AiGitGenError(f"git 명령 실행에 실패했습니다: {stderr or ' '.join(args)}")

    return (result.stdout, None) if allow_fail else result.stdout


def is_git_repo() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def get_status_short() -> str:
    """`git status --short` 출력을 반환한다."""
    return _run_git(["status", "--short"]).rstrip("\n")


def get_staged_diff() -> str:
    """스테이징된 변경사항의 diff. 스테이징된 게 없으면 빈 문자열."""
    return _run_git(["diff", "--staged"]).rstrip("\n")


def get_unstaged_diff() -> str:
    """스테이징되지 않은 변경사항의 diff."""
    return _run_git(["diff"]).rstrip("\n")


def get_commit_diff_for_commit_message() -> tuple:
    """커밋 메시지 생성에 쓸 (diff, source) 쌍을 반환한다.

    스테이징된 변경을 우선 사용하고, 없으면 워킹트리 변경으로 대체한다.
    둘 다 없으면 NoChangesError.
    """
    staged = get_staged_diff()
    if staged.strip():
        return staged, "staged"

    unstaged = get_unstaged_diff()
    if unstaged.strip():
        return unstaged, "unstaged"

    status = get_status_short()
    if status.strip():
        # diff는 비어있지만 untracked 파일 등 status 변화는 있는 경우
        return "", "status-only"

    raise NoChangesError("커밋할 변경 사항이 없습니다. 'git status'로 확인하세요.")


def get_current_branch() -> str:
    return _run_git(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def get_recent_commits(base_ref: str, max_count: int = 20) -> str:
    """base_ref 대비 현재 브랜치의 커밋 로그(제목만). base_ref가 없으면 최근 N개로 대체."""
    check = subprocess.run(
        ["git", "rev-parse", "--verify", base_ref],
        capture_output=True,
        text=True,
        check=False,
    )
    if check.returncode == 0:
        log = _run_git(["log", f"{base_ref}..HEAD", "--pretty=format:%s"])
        if log.strip():
            return log
    return _run_git(["log", f"-{max_count}", "--pretty=format:%s"])


def get_diff_for_pr(base_ref: str) -> tuple:
    """base_ref 대비 diff. base_ref가 없으면 마지막 커밋 diff로, 그마저 없으면
    (커밋이 1개뿐인 저장소) 빈 트리 대비 diff로 대체한다."""
    check = subprocess.run(
        ["git", "rev-parse", "--verify", base_ref],
        capture_output=True,
        text=True,
        check=False,
    )
    if check.returncode == 0:
        diff = _run_git(["diff", f"{base_ref}...HEAD"])
        if diff.strip():
            return diff, base_ref

    diff, err = _run_git(["diff", "HEAD~1", "HEAD"], allow_fail=True)
    if diff is not None:
        return diff, "HEAD~1"

    # 커밋이 1개뿐이라 HEAD~1이 존재하지 않는 경우: 빈 트리 대비 diff로 대체
    diff = _run_git(["diff", EMPTY_TREE_SHA, "HEAD"])
    return diff, "저장소 시작 시점(최초 커밋)"
