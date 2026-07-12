#!/usr/bin/env python3
"""AI 기반 Git 커밋 & PR 자동 생성기 — 진입점.

사용법:
    python main.py commit [--model ...] [--temperature ...] [--max-tokens ...] [--safe-mode]
    python main.py pr [--base origin/main] [--model ...] [--safe-mode]
"""

import sys

from ai_gitgen.cli import run

if __name__ == "__main__":
    sys.exit(run())
