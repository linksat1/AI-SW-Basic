"""safe-mode: 민감정보 마스킹(A)과 diff 전송량 제한(B).

기본 정책
- 마스킹: API Key/토큰/비밀번호/이메일/전화번호 형태를 정규표현식으로 치환
- 전송 제한: 최대 10개 파일, 최대 200줄
- 정책 값은 CLI 옵션 또는 컨벤션 파일(safe_mode 항목)로 조정할 수 있다.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

DEFAULT_MAX_FILES = 10
DEFAULT_MAX_LINES = 200

# (이름, 정규표현식, 치환 문자열). 더 구체적인 패턴을 먼저 적용한다.
BUILTIN_PATTERNS: List[Tuple[str, str, str]] = [
    ("anthropic_key", r"sk-ant-[A-Za-z0-9_-]{20,}", "[MASKED_ANTHROPIC_KEY]"),
    ("openai_style_key", r"sk-[A-Za-z0-9_-]{20,}", "[MASKED_API_KEY]"),
    ("aws_access_key", r"AKIA[0-9A-Z]{16}", "[MASKED_AWS_KEY]"),
    ("github_token", r"gh[pousr]_[A-Za-z0-9]{20,}", "[MASKED_GITHUB_TOKEN]"),
    ("slack_token", r"xox[baprs]-[A-Za-z0-9-]{10,}", "[MASKED_SLACK_TOKEN]"),
    ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "[MASKED_PRIVATE_KEY]"),
    ("secret_assignment",
     r"(?i)\b((?:api[_-]?key|access[_-]?token|secret|password|passwd|token)\s*[:=]\s*[\"']?)(?!\[MASKED)[^\s\"']+",
     r"\1[MASKED]"),
]
EMAIL_PATTERN = ("email", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[MASKED_EMAIL]")
PHONE_PATTERN = ("phone_kr", r"\b01[016789]-?\d{3,4}-?\d{4}\b", "[MASKED_PHONE]")


@dataclass
class SafeModePolicy:
    """safe-mode 정책. 숫자 기준은 파일 수와 diff 줄 수다."""

    max_files: int = DEFAULT_MAX_FILES
    max_lines: int = DEFAULT_MAX_LINES
    mask_emails: bool = True
    mask_phones: bool = True
    extra_patterns: List[str] = field(default_factory=list)

    def patterns(self) -> List[Tuple[str, str, str]]:
        result = list(BUILTIN_PATTERNS)
        if self.mask_emails:
            result.append(EMAIL_PATTERN)
        if self.mask_phones:
            result.append(PHONE_PATTERN)
        for i, pattern in enumerate(self.extra_patterns, 1):
            result.append((f"custom_{i}", pattern, "[MASKED_CUSTOM]"))
        return result


@dataclass
class SafeModeResult:
    text: str
    masked: Dict[str, int]
    total_files: int
    sent_files: int
    total_lines: int
    sent_lines: int

    def summary(self) -> str:
        masked = ", ".join(f"{k} x{v}" for k, v in self.masked.items()) or "없음"
        return (f"마스킹: {masked} | 파일 {self.sent_files}/{self.total_files}개 전송 | "
                f"diff {self.sent_lines}/{self.total_lines}줄 전송")


def validate_patterns(patterns: List[str]) -> None:
    """사용자 정의 정규표현식이 컴파일되는지 확인한다."""
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"잘못된 마스킹 정규표현식 '{pattern}': {exc}") from exc


def mask_sensitive_text(text: str, policy: SafeModePolicy) -> Tuple[str, Dict[str, int]]:
    """정책의 패턴을 순서대로 적용해 민감정보를 치환하고 패턴별 적중 횟수를 반환한다."""
    hits: Dict[str, int] = {}
    for name, pattern, replacement in policy.patterns():
        text, count = re.subn(pattern, replacement, text)
        if count:
            hits[name] = count
    return text, hits


def split_diff_by_file(diff_text: str) -> List[str]:
    """`diff --git` 헤더를 기준으로 diff를 파일 단위 조각으로 나눈다."""
    chunks: List[str] = []
    current: List[str] = []
    for line in diff_text.splitlines():
        if line.startswith("diff --git ") and current:
            chunks.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        chunks.append("\n".join(current))
    return chunks


def limit_diff(diff_text: str, max_files: int, max_lines: int) -> Tuple[str, int, int, int, int]:
    """파일 수와 줄 수 기준으로 diff를 자른다. (text, 전체파일, 전송파일, 전체줄, 전송줄)"""
    chunks = split_diff_by_file(diff_text)
    total_lines = len(diff_text.splitlines())
    kept_chunks = chunks[:max_files]

    lines: List[str] = []
    for chunk in kept_chunks:
        lines.extend(chunk.splitlines())
    sent_lines = min(len(lines), max_lines)
    text = "\n".join(lines[:max_lines])

    notes = []
    if len(chunks) > max_files:
        notes.append(f"파일 {len(chunks)}개 중 {max_files}개만 전송")
    if total_lines > sent_lines:
        notes.append(f"전체 {total_lines}줄 중 {sent_lines}줄만 전송")
    if notes:
        text += f"\n\n... (safe-mode: {', '.join(notes)}) ..."
    return text, len(chunks), len(kept_chunks), total_lines, sent_lines


def apply_safe_mode(diff_text: str, policy: SafeModePolicy) -> SafeModeResult:
    """마스킹 후 전송량을 제한한다."""
    masked_text, hits = mask_sensitive_text(diff_text, policy)
    text, total_files, sent_files, total_lines, sent_lines = limit_diff(
        masked_text, policy.max_files, policy.max_lines)
    return SafeModeResult(text, hits, total_files, sent_files, total_lines, sent_lines)
