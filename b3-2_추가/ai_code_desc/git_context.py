"""Git 변경사항 수집 모듈.

수집 범위는 과제 제약에 따라 `git status`, `git diff`로 한정한다.
"""

import os
import subprocess
from dataclasses import dataclass, field
from typing import List


class GitError(RuntimeError):
    """Git 명령 실행 또는 저장소 위치 검사 실패."""


@dataclass
class GitContext:
    """AI 프롬프트의 입력이 되는 Git 변경 정보."""

    root: str
    status_text: str
    diff_text: str
    files: List[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.status_text.strip() or self.diff_text.strip())

    @property
    def diff_line_count(self) -> int:
        return len(self.diff_text.splitlines())


def _run_git(args: List[str], cwd: str, ok_codes=(0,)) -> str:
    """git 명령을 실행하고 stdout을 반환한다. 허용되지 않은 종료 코드는 GitError."""
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", *args],
            cwd=cwd, capture_output=True, text=True, check=False,
        )
    except FileNotFoundError as exc:
        raise GitError("git 명령을 찾을 수 없습니다. Git을 설치하세요.") from exc
    if result.returncode not in ok_codes:
        stderr = result.stderr.strip() or " ".join(args)
        raise GitError(f"git 명령 실행 오류: {stderr}")
    return result.stdout.rstrip("\n")


def find_repo_root(cwd: str) -> str:
    """cwd가 Git 저장소 루트인지 확인하고 루트 경로를 반환한다."""
    try:
        root = _run_git(["rev-parse", "--show-toplevel"], cwd)
    except GitError as exc:
        raise GitError("현재 디렉터리는 git 저장소가 아닙니다. 프로젝트 루트에서 실행하세요.") from exc
    if os.path.realpath(root) != os.path.realpath(cwd):
        raise GitError(f"프로젝트 루트 디렉터리에서 실행하세요. (저장소 루트: {root})")
    return root


def parse_status_files(status_text: str) -> List[str]:
    """`git status --porcelain` 출력에서 변경 파일 경로 목록을 추출한다."""
    files: List[str] = []
    for line in status_text.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:  # rename: "old -> new"
            path = path.split(" -> ", 1)[1]
        files.append(path.strip('"'))
    return files


def collect_git_context(cwd: str = None) -> GitContext:
    """git status와 git diff(unstaged + staged + untracked)를 수집한다."""
    cwd = cwd or os.getcwd()
    root = find_repo_root(cwd)

    status_text = _run_git(["status", "--porcelain", "--untracked-files=all"], root)
    files = parse_status_files(status_text)

    parts = []
    unstaged = _run_git(["diff"], root)
    if unstaged.strip():
        parts.append(unstaged)
    staged = _run_git(["diff", "--cached"], root)
    if staged.strip():
        parts.append(staged)

    # 새로 추가된(untracked) 파일은 git diff에 나오지 않으므로 --no-index로 비교한다.
    for line in status_text.splitlines():
        if line.startswith("?? "):
            path = parse_status_files(line)[0]
            # 차이가 있으면 종료 코드 1을 반환하는 것이 정상 동작이다.
            text = _run_git(["diff", "--no-index", "--", os.devnull, path], root, ok_codes=(0, 1))
            if text.strip():
                parts.append(text)

    return GitContext(root=root, status_text=status_text, diff_text="\n".join(parts), files=files)
