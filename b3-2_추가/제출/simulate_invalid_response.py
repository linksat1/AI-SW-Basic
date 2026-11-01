"""검증 실패 시 재생성/후처리 흐름을 보여주는 시연 스크립트.

실제 API 대신 형식이 틀린 응답을 두 번 돌려주도록 call_model을 바꿔 끼운다.
사용: python 제출/simulate_invalid_response.py <변경 사항이 있는 git 저장소 루트>
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai_code_desc import ai_client, cli  # noqa: E402

BAD_RESPONSES = [
    # 1회차: 제목 72자 초과, 헤더/불릿 표기가 다르고(### , *), 섹션 3개 누락
    "TITLE: feat: " + "세션 처리 로직과 예외 처리, 로그 포맷, 테스트 분기를 정리한 " * 2 + "변경\n"
    "BODY:\n### Summary\n* 세션 검증을 강화했습니다.\n",
    # 2회차: 제목은 고쳤지만 How to Verify에 불릿이 없음
    "TITLE: feat: 세션 검증 및 예외 처리 보완\nBODY:\n## Summary\n- 세션 검증을 강화했습니다.\n"
    "## What Changed\n- session.py에 SessionError를 추가했습니다.\n## Why It Was Needed\n- 빈 사용자 입력을 막습니다.\n"
    "## How to Verify\n빈 문자열로 create_session을 호출해 보세요.\n",
]


def main() -> int:
    os.chdir(sys.argv[1])
    args = cli.build_parser().parse_args(["describe", "--intent", "세션 검증과 예외 처리 보완"])
    print("[SIMULATION] AI 응답 대신 형식이 틀린 응답 2개를 순서대로 사용합니다.")
    with patch.object(ai_client, "ensure_ready"), \
         patch.object(ai_client, "call_model", side_effect=BAD_RESPONSES) as call:
        code = cli.describe_command(args)
    print(f"[SIMULATION] call_model 호출 횟수: {call.call_count}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
