"""팀 컨벤션(설명 템플릿 커스터마이징) 로딩.

우선순위: --convention <경로> > 저장소 루트의 .ai-code-summary.json > 기본 컨벤션
설정 파일은 표준 라이브러리만으로 읽을 수 있도록 JSON 형식을 사용한다.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

from .safe_mode import SafeModePolicy, validate_patterns

CONVENTION_FILENAME = ".ai-code-summary.json"


@dataclass
class Convention:
    """설명문 제목/본문 규칙과 safe-mode 정책 기본값."""

    name: str = "기본 컨벤션 (Conventional Commits)"
    title_prefixes: List[str] = field(default_factory=lambda: [
        "feat", "fix", "refactor", "docs", "test", "chore"])
    title_style: str = "'<type>: <한국어 요약>' 형식 (예: feat: 사용자 세션 처리 보완)"
    title_recommended_length: int = 50
    title_max_length: int = 72
    language: str = "한국어"
    max_bullets_per_section: int = 3
    rules: List[str] = field(default_factory=list)
    safe_mode: SafeModePolicy = field(default_factory=SafeModePolicy)
    source: str = "내장 기본값"

    def prompt_rules(self) -> List[str]:
        """프롬프트에 넣을 컨벤션 규칙 문장 목록."""
        lines = [
            f"제목 형식: {self.title_style}",
            f"제목 길이: {self.title_recommended_length}자 이내 권장, 최대 {self.title_max_length}자",
            f"작성 언어: {self.language}",
            f"각 섹션 불릿 수: 1~{self.max_bullets_per_section}개",
        ]
        if self.title_prefixes:
            lines.append("제목 접두어(아래 중 하나로 시작): " + ", ".join(self.title_prefixes))
        lines.extend(self.rules)
        return lines


def _load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fp:
            data = json.load(fp)
    except OSError as exc:
        raise ValueError(f"컨벤션 파일을 열 수 없습니다: {path} ({exc.strerror})") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"컨벤션 파일 JSON 형식 오류: {path} (line {exc.lineno}: {exc.msg})") from exc
    if not isinstance(data, dict):
        raise ValueError(f"컨벤션 파일 최상위는 객체여야 합니다: {path}")
    return data


def convention_from_dict(data: dict, source: str) -> Convention:
    """JSON dict를 Convention으로 변환한다. 없는 항목은 기본값을 쓴다."""
    base = Convention()
    sm = data.get("safe_mode", {}) or {}
    extra = list(sm.get("extra_mask_patterns", []))
    validate_patterns(extra)
    policy = SafeModePolicy(
        max_files=int(sm.get("max_files", base.safe_mode.max_files)),
        max_lines=int(sm.get("max_lines", base.safe_mode.max_lines)),
        mask_emails=bool(sm.get("mask_emails", True)),
        mask_phones=bool(sm.get("mask_phones", True)),
        extra_patterns=extra,
    )
    conv = Convention(
        name=data.get("name", base.name),
        title_prefixes=list(data.get("title_prefixes", base.title_prefixes)),
        title_style=data.get("title_style", base.title_style),
        title_recommended_length=int(data.get("title_recommended_length", base.title_recommended_length)),
        title_max_length=int(data.get("title_max_length", base.title_max_length)),
        language=data.get("language", base.language),
        max_bullets_per_section=int(data.get("max_bullets_per_section", base.max_bullets_per_section)),
        rules=list(data.get("rules", [])),
        safe_mode=policy,
        source=source,
    )
    if conv.title_max_length > 72 or conv.title_recommended_length > conv.title_max_length:
        raise ValueError("컨벤션 제목 길이는 '권장 <= 최대 <= 72'를 만족해야 합니다.")
    return conv


def load_convention(repo_root: str, path: Optional[str] = None) -> Convention:
    """지정 경로 또는 저장소 루트의 컨벤션 파일을 읽는다. 둘 다 없으면 기본값."""
    if path:
        return convention_from_dict(_load_json(path), path)
    default_path = os.path.join(repo_root, CONVENTION_FILENAME)
    if os.path.isfile(default_path):
        return convention_from_dict(_load_json(default_path), default_path)
    return Convention()
