"""safe-mode: 민감정보 마스킹 + 전송 diff 크기 제한."""

import re

# (설명, 정규식, 대체 문자열) — 흔한 시크릿 포맷을 정규식으로 탐지해 마스킹한다.
_SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}"), "[MASKED_AWS_ACCESS_KEY]"),
    ("Anthropic API Key", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "[MASKED_ANTHROPIC_KEY]"),
    ("OpenAI API Key", re.compile(r"sk-[A-Za-z0-9]{20,}"), "[MASKED_API_KEY]"),
    ("GitHub Token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "[MASKED_GITHUB_TOKEN]"),
    ("Slack Token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "[MASKED_SLACK_TOKEN]"),
    (
        "Generic key=value secret",
        re.compile(
            r"""(?ix)
            \b(api[_-]?key|secret|token|password|passwd|access[_-]?key)
            \s*[:=]\s*
            ["']?([A-Za-z0-9_\-/+=.]{8,})["']?
            """
        ),
        None,  # 그룹1(키 이름)은 유지, 그룹2(값)만 마스킹 — apply_mask에서 처리
    ),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "[MASKED_PRIVATE_KEY_HEADER]"),
]


def mask_secrets(text: str) -> tuple:
    """텍스트에서 민감정보로 추정되는 패턴을 마스킹한다.

    반환: (마스킹된 텍스트, 마스킹된 항목 설명 리스트)
    """
    masked_kinds = []
    result = text

    for name, pattern, replacement in _SECRET_PATTERNS:
        if replacement is not None:
            new_result, count = pattern.subn(replacement, result)
        else:
            def _mask_value(m):
                return f"{m.group(1)}={'*' * min(len(m.group(2)), 8)}"

            new_result, count = pattern.subn(_mask_value, result)

        if count:
            masked_kinds.append(f"{name} x{count}")
        result = new_result

    return result, masked_kinds


def limit_diff(text: str, max_lines: int = 400) -> tuple:
    """diff를 max_lines 줄까지만 남기고 자른다.

    반환: (제한된 텍스트, 잘렸는지 여부, 원본 줄 수)
    """
    lines = text.splitlines()
    total = len(lines)
    if total <= max_lines:
        return text, False, total

    truncated = "\n".join(lines[:max_lines])
    truncated += (
        f"\n\n... (safe-mode: 전체 {total}줄 중 {max_lines}줄만 전송, "
        f"{total - max_lines}줄 생략) ..."
    )
    return truncated, True, total


def apply_safe_mode(diff_text: str, max_lines: int = 400) -> dict:
    """마스킹 + 크기 제한을 모두 적용하고 요약 정보를 반환한다."""
    masked_text, masked_kinds = mask_secrets(diff_text)
    limited_text, truncated, total_lines = limit_diff(masked_text, max_lines=max_lines)
    return {
        "text": limited_text,
        "masked_kinds": masked_kinds,
        "truncated": truncated,
        "total_lines": total_lines,
        "sent_lines": min(total_lines, max_lines),
    }
