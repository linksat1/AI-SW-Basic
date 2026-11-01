"""프롬프트 구성, 응답 파싱, 형식 검증/다듬기, 결과 출력."""

import re
from dataclasses import dataclass, field
from typing import List, Tuple

from .convention import Convention

VERSION = "0.2.0"
REQUIRED_SECTIONS = ["Summary", "What Changed", "Why It Was Needed", "How to Verify"]
MISSING_BULLET = "- (AI 응답에 없던 항목입니다. 검토 후 직접 작성하세요.)"
BAR = "-" * 22

SYSTEM_PROMPT = """당신은 코드 리뷰와 발표 자료를 돕는 시니어 소프트웨어 엔지니어입니다.
사용자가 준 Git 변경 사항(diff)과 수정 의도를 근거로, 리뷰어가 바로 읽을 수 있는 코드 설명 초안을 작성합니다.
diff에 없는 내용을 지어내지 말고, 근거가 부족하면 그 섹션에 확인이 필요하다고 적으세요.
'[MASKED_...]'로 표시된 값은 보안상 가린 값이므로 원래 값을 추측하지 마세요.
답변은 사용자가 지정한 TITLE/BODY 형식만 사용하고, 인사말이나 코드블록 감싸기를 붙이지 않습니다."""


@dataclass
class Description:
    title: str
    body: str


@dataclass
class ValidationReport:
    errors: List[str] = field(default_factory=list)    # 필수 규칙 위반 -> 재생성/보정 대상
    warnings: List[str] = field(default_factory=list)  # 권장 규칙 위반 -> 안내만

    @property
    def ok(self) -> bool:
        return not self.errors


def build_user_prompt(status_text: str, files: List[str], diff_text: str, intent: str,
                      convention: Convention, feedback: List[str] = None) -> str:
    """변경 정보 + 수정 의도 + 출력 규칙을 하나의 사용자 프롬프트로 묶는다."""
    file_list = "\n".join(f"- {f}" for f in files) or "(없음)"
    parts = [
        "## 수정 의도 (작성자 입력)",
        intent or "(입력 없음 - diff만 보고 의도를 추론하되, 추론임을 드러내세요)",
        "",
        f"## 변경 파일 목록 ({len(files)}개, git status)",
        file_list,
        "",
        "## git status --porcelain",
        status_text or "(없음)",
        "",
        "## git diff",
        diff_text or "(diff 없음)",
        "",
        "## 작성 규칙",
        *[f"- {rule}" for rule in convention.prompt_rules()],
        "- What Changed에는 변경된 파일(또는 모듈) 1~3개를 이름으로 언급하세요.",
        "- How to Verify에는 리뷰어가 실제로 실행할 수 있는 확인 방법을 쓰세요.",
        "",
        "## 출력 형식 (이 형식만 사용)",
        "TITLE: <제목 한 줄>",
        "BODY:",
    ]
    for section in REQUIRED_SECTIONS:
        parts += [f"## {section}", "- <불릿>", ""]
    if feedback:
        parts += ["## 이전 응답의 형식 오류 (반드시 고쳐서 다시 작성)", *[f"- {p}" for p in feedback]]
    return "\n".join(parts).rstrip() + "\n"


def generate_mock_response(files: List[str], intent: str, convention: Convention) -> str:
    """API 없이 흐름을 확인하기 위한 데모 응답. 실제 변경 파일과 의도, 컨벤션을 반영한다."""
    summary = (intent or "코드 변경 사항 정리").strip().split("\n")[0]
    summary = re.split(r"[.,]", summary)[0].strip() or "코드 변경 사항 정리"
    prefix = convention.title_prefixes[0] if convention.title_prefixes else ""
    if not prefix:
        title = summary
    elif prefix[0].islower():
        title = f"{prefix}: {summary}"
    else:
        title = f"{prefix} {summary}"
    shown = files[:3] or ["(변경 파일 없음)"]
    changed = "\n".join(f"- `{f}` 변경" for f in shown)
    body = f"""## Summary
- 수정 의도 요약: {summary}
- (mock 응답입니다. 실제 AI 분석 결과가 아닙니다.)

## What Changed
{changed}

## Why It Was Needed
- 작성자 입력: {intent or '(입력 없음)'}

## How to Verify
- 변경 파일 {len(files)}개의 diff를 `git diff`로 확인합니다.
- API Key를 설정한 뒤 `--mock` 없이 실행해 실제 AI 설명을 생성합니다."""
    return f"TITLE: {title}\nBODY:\n{body}"


def parse_title_body(raw_text: str) -> Description:
    """'TITLE: ... / BODY: ...' 응답을 제목과 본문으로 분리한다. 형식이 없으면 첫 줄을 제목으로."""
    text = raw_text.strip()
    text = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text).strip()
    title_match = re.search(r"^\**TITLE\**\s*:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    body_match = re.search(r"^\**BODY\**\s*:\s*\n?(.*)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        body = body_match.group(1) if body_match else text[title_match.end():]
    else:
        lines = text.splitlines()
        title = lines[0] if lines else ""
        body = "\n".join(lines[1:])
    return Description(title=title.strip(), body=body.strip())


def normalize(desc: Description) -> Description:
    """내용을 바꾸지 않는 형식 정리: 헤더/불릿 표기 통일, 제목 한 줄화."""
    title = re.sub(r"^[#*\s\"'`]+|[*\s\"'`]+$", "", desc.title).strip()
    lines = []
    for line in desc.body.splitlines():
        stripped = line.strip()
        header = re.match(r"^(?:#{1,6}\s*|\*\*)?\s*(" + "|".join(REQUIRED_SECTIONS) +
                          r")\s*(?:\*\*)?\s*:?\s*(?:\(.*\))?$", stripped, re.IGNORECASE)
        if header:
            canonical = next(s for s in REQUIRED_SECTIONS if s.lower() == header.group(1).lower())
            lines.append(f"## {canonical}")
        elif re.match(r"^[*•·]\s+", stripped):
            lines.append("- " + re.sub(r"^[*•·]\s+", "", stripped))
        else:
            lines.append(line.rstrip())
    return Description(title=title, body="\n".join(lines).strip())


def split_sections(body: str) -> List[Tuple[str, List[str]]]:
    """'## 헤더' 기준으로 (헤더, 줄 목록) 리스트를 만든다."""
    sections: List[Tuple[str, List[str]]] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            sections.append((m.group(1), []))
        elif sections:
            sections[-1][1].append(line)
    return sections


def validate(desc: Description, convention: Convention) -> ValidationReport:
    """제목 길이/본문 섹션/불릿 규칙을 검사한다."""
    report = ValidationReport()
    title = desc.title
    if not title:
        report.errors.append("설명 제목이 비어 있습니다.")
    elif "\n" in title:
        report.errors.append("설명 제목은 1줄이어야 합니다.")
    elif len(title) > convention.title_max_length:
        report.errors.append(f"설명 제목이 최대 {convention.title_max_length}자를 초과합니다 ({len(title)}자).")
    elif len(title) > convention.title_recommended_length:
        report.warnings.append(f"설명 제목이 권장 {convention.title_recommended_length}자를 넘습니다 ({len(title)}자).")
    if title and convention.title_prefixes and not any(title.startswith(p) for p in convention.title_prefixes):
        report.warnings.append("제목이 컨벤션 접두어로 시작하지 않습니다: " + ", ".join(convention.title_prefixes))

    sections = dict(split_sections(desc.body))
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            report.errors.append(f"'{name}' 섹션 헤더가 없습니다.")
            continue
        bullets = [l for l in sections[name] if re.match(r"^\s*-\s+\S", l)]
        top_level = [l for l in bullets if re.match(r"^-\s", l)]  # 들여쓴 하위 불릿은 개수에서 제외
        if not bullets:
            report.errors.append(f"'{name}' 섹션에 불릿이 1개 이상 필요합니다.")
        elif len(top_level) > convention.max_bullets_per_section:
            report.warnings.append(f"'{name}' 섹션 불릿이 {len(top_level)}개로 권장 "
                                   f"{convention.max_bullets_per_section}개를 넘습니다.")
    return report


def repair(desc: Description, convention: Convention) -> Description:
    """재생성 후에도 남은 필수 규칙 위반을 후처리로 보정한다."""
    title = desc.title.splitlines()[0].strip() if desc.title else ""
    if not title:
        title = "docs: 코드 변경 설명 (제목 검토 필요)"
    if len(title) > convention.title_max_length:
        title = title[:convention.title_max_length - 1].rstrip() + "…"

    found = dict(split_sections(desc.body))
    out: List[str] = []
    for name in REQUIRED_SECTIONS:
        lines = [l for l in found.get(name, []) if l.strip()]
        bullets = [l.strip() for l in lines if re.match(r"^\s*-\s+\S", l)]
        if not bullets:
            # 불릿이 없으면 일반 문장을 불릿으로 바꾸고, 그것도 없으면 검토 안내 불릿을 넣는다.
            bullets = [f"- {l.strip()}" for l in lines] or [MISSING_BULLET]
        out += [f"## {name}", *bullets, ""]
    return Description(title=title, body="\n".join(out).strip())


def render(desc: Description, report: ValidationReport, footer: List[str]) -> str:
    """사용자가 복사하기 쉽도록 제목/본문/검증 결과를 구획을 나눠 출력한다."""
    lines = [
        f"--- Description Title --- ({len(desc.title)}자)",
        desc.title,
        "",
        "--- Description Body ---",
        desc.body,
        BAR,
        "",
        "--- Validation ---",
    ]
    if report.ok:
        lines.append("[OK] 제목 길이/섹션 헤더/섹션별 불릿 검증 통과")
    for err in report.errors:
        lines.append(f"[FAIL] {err}")
    for warn in report.warnings:
        lines.append(f"[WARN] {warn}")
    lines += footer
    lines.append("[NOTE] 생성된 설명은 초안입니다. 내용을 검토한 뒤 적용하세요.")
    return "\n".join(lines)
