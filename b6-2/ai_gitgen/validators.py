"""AI 응답 파싱 + 길이/형식 검증."""

import re

COMMIT_TITLE_MAX = 72
PR_TITLE_MAX = 80

REQUIRED_PR_SECTIONS = ["Why", "What", "How to Test"]


def parse_title_body(raw_text: str) -> tuple:
    """"TITLE: ...\\nBODY:\\n..." 형식의 응답을 (title, body)로 분리한다."""
    text = raw_text.strip()

    title_match = re.search(r"^TITLE:\s*(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    body_match = re.search(r"^BODY:\s*\n(.*)", text, re.MULTILINE | re.DOTALL)
    body = body_match.group(1).strip() if body_match else ""

    if not title:
        # 형식을 못 지킨 응답에 대한 최후 방어: 첫 줄을 제목으로 사용
        lines = text.splitlines()
        title = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]).strip()

    return title, body


def validate_commit(title: str, body: str) -> list:
    problems = []
    if not title:
        problems.append("커밋 제목이 비어 있습니다.")
    elif len(title) > COMMIT_TITLE_MAX:
        problems.append(f"커밋 제목이 {COMMIT_TITLE_MAX}자를 초과합니다 ({len(title)}자).")
    if title.endswith("."):
        problems.append("커밋 제목은 마침표로 끝나지 않아야 합니다.")
    return problems


def validate_pr(title: str, body: str) -> list:
    problems = []
    if not title:
        problems.append("PR 제목이 비어 있습니다.")
    elif len(title) > PR_TITLE_MAX:
        problems.append(f"PR 제목이 {PR_TITLE_MAX}자를 초과합니다 ({len(title)}자).")

    for section in REQUIRED_PR_SECTIONS:
        pattern = re.compile(
            rf"^##\s*{re.escape(section)}\s*\n((?:.*\n?)*?)(?=^##\s|\Z)",
            re.MULTILINE,
        )
        match = pattern.search(body)
        if not match:
            problems.append(f"'{section}' 섹션이 없습니다.")
            continue
        section_body = match.group(1)
        bullets = re.findall(r"^\s*-\s+\S", section_body, re.MULTILINE)
        if not bullets:
            problems.append(f"'{section}' 섹션에 불릿(- 항목)이 1개 이상 필요합니다.")

    return problems
