"""Mini Git REPL(Read-Eval-Print Loop) CLI.

`mini-git> ` 프롬프트에서 한 줄을 읽어(1) 토큰으로 나누고, (2) Repository의
메서드를 호출해 실행한 뒤, (3) 사람이 읽기 좋은 문자열로 결과를 출력하는
과정을 exit/quit이 입력될 때까지 반복한다.

Repository/traversal/sorting/index는 "무엇을 어떻게 저장·탐색·정렬할지"만
알고 사용자 입력 형식이나 화면 출력 형식은 전혀 모른다. 이 파일이 그
사이의 번역(입력 파싱 + 출력 포맷팅)을 전담한다.
"""

import shlex

from mini_git.errors import MiniGitError
from mini_git.repository import Repository

PROMPT = "mini-git> "


# ======================================================================
# 출력 포맷터
# ======================================================================

def _format_log(commits, show_branch=True):
    """LOG / LOG --sort-by=... 공통 출력 포맷.

    "commit <hash> (<author>, <timestamp>) [<branch>]" 다음 줄에 메시지,
    커밋마다 이를 반복한다. hash/author/timestamp/message가 전부 식별
    가능해야 한다는 과제 요구를 만족한다. [<branch>]는 필수 항목은
    아니지만(과제 예시에는 --sort-by 결과에서 생략됨) 정보량이 늘어나는
    확장이라 판단해 두 출력 모두에서 일관되게 보여준다.
    """
    if not commits:
        return "(no commits)"
    lines = []
    for c in commits:
        if show_branch:
            lines.append(
                "commit {} ({}, {}) [{}]".format(
                    c.hash, c.author, c.formatted_timestamp(), c.branch
                )
            )
        else:
            lines.append(
                "commit {} ({}, {})".format(c.hash, c.author, c.formatted_timestamp())
            )
        lines.append(c.message)
    return "\n".join(lines)


def _format_search_results(results):
    """SEARCH / SEARCH --author=... 공통 출력 포맷."""
    count = len(results)
    label = "commit" if count == 1 else "commits"
    lines = ["Found {} {}:".format(count, label), ""]
    for c in results:
        lines.append("- {}: {}".format(c.hash, c.message))
    return "\n".join(lines)


# ======================================================================
# 명령어 핸들러
# 각 핸들러는 (repo, args) -> 출력할 문자열 시그니처를 갖는다.
# ======================================================================

def _cmd_init(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    repo.init(args[0])
    return "Initialized repository.\nCurrent branch: {}\nCurrent user: {}".format(
        repo.current_branch, repo.current_user
    )


def _cmd_branch(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    repo.branch(args[0])
    return "Created branch: {}".format(args[0])


def _cmd_switch(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    repo.switch(args[0])
    return "Switched to branch: {}".format(args[0])


def _cmd_commit(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    c = repo.commit(args[0])
    return "[{} {}] {}".format(c.branch, c.hash, c.message)


def _cmd_log(repo: Repository, args):
    if len(args) == 0:
        return _format_log(repo.log(), show_branch=True)

    if len(args) == 1 and args[0].startswith("--sort-by="):
        by = args[0].split("=", 1)[1]
        if by not in ("date", "author"):
            return "Invalid args"
        return _format_log(repo.log_sorted(by), show_branch=True)

    return "Invalid args"


def _cmd_path(repo: Repository, args):
    if len(args) != 2:
        return "Invalid args"
    path = repo.shortest_path(args[0], args[1])
    if path is None:
        return "No path"
    return "Path: " + " -> ".join(path)


def _cmd_ancestors(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    result = repo.ancestors(args[0])
    if not result:
        return "No ancestors."
    lines = ["Ancestors of {}:".format(args[0])]
    for h in result:
        lines.append("- " + h)
    return "\n".join(lines)


def _cmd_search(repo: Repository, args):
    if len(args) != 1:
        return "Invalid args"
    token = args[0]
    if token.startswith("--author="):
        name = token.split("=", 1)[1]
        results = repo.search_author(name)
    else:
        results = repo.search_keyword(token)
    return _format_search_results(results)


def dispatch(repo: Repository, raw_line: str) -> str:
    """한 줄 입력을 파싱해 실행하고, 출력할 문자열을 반환한다."""
    try:
        tokens = shlex.split(raw_line)
    except ValueError:
        return "Invalid args"  # 예: 따옴표 짝이 안 맞음

    if not tokens:
        return ""

    cmd = tokens[0].upper()  # 명령어는 대소문자 구분 없음
    args = tokens[1:]

    try:
        if cmd == "INIT":
            return _cmd_init(repo, args)
        elif cmd == "BRANCH":
            return _cmd_branch(repo, args)
        elif cmd == "SWITCH":
            return _cmd_switch(repo, args)
        elif cmd == "COMMIT":
            return _cmd_commit(repo, args)
        elif cmd == "LOG":
            return _cmd_log(repo, args)
        elif cmd == "PATH":
            return _cmd_path(repo, args)
        elif cmd == "ANCESTORS":
            return _cmd_ancestors(repo, args)
        elif cmd == "SEARCH":
            return _cmd_search(repo, args)
        else:
            return "Invalid args"  # 알 수 없는 명령도 표준 에러 셋 중 하나로 처리
    except MiniGitError as e:
        return str(e)


def run() -> None:
    """REPL 진입점. exit 또는 quit을 입력할 때까지 명령을 계속 받는다."""
    repo = Repository()
    print("Mini Git CLI — 종료하려면 exit 또는 quit을 입력하세요.")
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
        result = dispatch(repo, stripped)
        if result:
            print(result)
