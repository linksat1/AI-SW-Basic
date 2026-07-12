"""AI API에 보낼 시스템/유저 프롬프트를 구성한다."""

COMMIT_SYSTEM_PROMPT = """당신은 숙련된 소프트웨어 엔지니어의 커밋 메시지 작성을 돕는 도우미입니다.
주어진 git status와 diff를 분석해 Conventional Commits 스타일의 커밋 메시지를 작성하세요.

규칙:
1. 제목(title)은 "type: 요약" 형식이며 72자를 넘지 않아야 합니다. type은 feat/fix/docs/refactor/test/chore 중 하나를 사용하세요.
2. 제목은 명령형(예: "add", "fix")으로 시작하고, 끝에 마침표를 붙이지 않습니다.
3. 본문(body)은 선택 사항이며, 필요할 때만 "왜" 바꿨는지 1~3줄로 설명합니다.
4. 반드시 아래 형식으로만 응답하세요. 다른 설명, 마크다운 코드블록, 인사말을 절대 덧붙이지 마세요.

TITLE: <커밋 제목>
BODY:
<커밋 본문 — 없으면 이 줄을 비워둠>
"""

PR_SYSTEM_PROMPT = """당신은 숙련된 소프트웨어 엔지니어의 Pull Request 작성을 돕는 도우미입니다.
주어진 커밋 로그와 diff를 분석해 리뷰어가 이해하기 쉬운 PR 제목과 본문을 작성하세요.

규칙:
1. 제목(title)은 80자를 넘지 않아야 합니다.
2. 본문은 반드시 아래 3개 섹션을 포함하며, 각 섹션에는 "- " 로 시작하는 불릿을 최소 1개 이상 작성합니다.
   - Why (왜 이 변경이 필요한가)
   - What (무엇을 변경했는가)
   - How to Test (어떻게 검증하는가)
3. 반드시 아래 형식으로만 응답하세요. 다른 설명, 마크다운 코드블록, 인사말을 절대 덧붙이지 마세요.

TITLE: <PR 제목>
BODY:
## Why
- <이유 1>

## What
- <변경 사항 1>

## How to Test
- <검증 방법 1>
"""


def build_commit_user_prompt(status_text: str, diff_text: str, diff_source: str) -> str:
    source_note = {
        "staged": "아래는 스테이징된(git add된) 변경사항입니다.",
        "unstaged": "스테이징된 변경이 없어 워킹트리의 변경사항을 대신 사용합니다.",
        "status-only": "diff는 비어 있지만 파일 상태 변화(예: 새 파일 추가)가 있습니다.",
    }.get(diff_source, "")

    parts = [source_note, "", "## git status --short", status_text or "(비어 있음)"]
    if diff_text:
        parts += ["", "## git diff", diff_text]
    return "\n".join(parts)


def build_pr_user_prompt(commit_log: str, diff_text: str, base_ref: str) -> str:
    parts = [
        f"기준 브랜치/커밋: {base_ref}",
        "",
        "## 포함된 커밋 목록",
        commit_log or "(커밋 로그 없음 — diff만 참고)",
        "",
        "## 변경 diff",
        diff_text or "(diff 없음)",
    ]
    return "\n".join(parts)
