"""CLI 진입점: `python main.py commit` / `python main.py pr`."""

import argparse
import sys

from . import ai_client, git_utils, prompt_builder, safe_mode, validators, formatter
from .errors import AiGitGenError


def _add_common_options(sub):
    sub.add_argument("--model", default=ai_client.DEFAULT_MODEL, help=f"사용할 모델 (기본값: {ai_client.DEFAULT_MODEL})")
    sub.add_argument("--temperature", type=float, default=None, help="샘플링 temperature (일부 모델은 미지원 — 기본값: 모델 기본값 사용)")
    sub.add_argument("--max-tokens", type=int, default=ai_client.DEFAULT_MAX_TOKENS, help=f"최대 출력 토큰 수 (기본값: {ai_client.DEFAULT_MAX_TOKENS})")
    sub.add_argument("--safe-mode", action="store_true", help="민감정보 마스킹 + diff 크기 제한을 적용해 전송")
    sub.add_argument("--max-diff-lines", type=int, default=400, help="safe-mode에서 전송할 diff 최대 줄 수 (기본값: 400)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="AI 기반 Git 커밋 메시지 / PR 초안 자동 생성기",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    commit_parser = subparsers.add_parser("commit", help="스테이징(또는 워킹트리) 변경사항으로 커밋 메시지 생성")
    _add_common_options(commit_parser)

    pr_parser = subparsers.add_parser("pr", help="브랜치 변경사항으로 PR 제목/본문 생성")
    pr_parser.add_argument("--base", default="origin/main", help="비교 기준 브랜치/커밋 (기본값: origin/main)")
    _add_common_options(pr_parser)

    return parser


def _prepare_diff_for_sending(diff_text: str, args) -> tuple:
    """safe-mode 적용 여부에 따라 전송용 diff와 메타 정보를 만든다."""
    if args.safe_mode:
        result = safe_mode.apply_safe_mode(diff_text, max_lines=args.max_diff_lines)
        meta = {
            "safe_mode": True,
            "masked_kinds": result["masked_kinds"],
            "truncated": result["truncated"],
            "total_lines": result["total_lines"],
            "sent_lines": result["sent_lines"],
        }
        return result["text"], meta
    return diff_text, {"safe_mode": False}


def cmd_commit(args) -> int:
    if not git_utils.is_git_repo():
        raise AiGitGenError("현재 디렉터리는 git 저장소가 아닙니다.")

    status_text = git_utils.get_status_short()
    diff_text, diff_source = git_utils.get_commit_diff_for_commit_message()

    sendable_diff, diff_meta = _prepare_diff_for_sending(diff_text, args)
    user_prompt = prompt_builder.build_commit_user_prompt(status_text, sendable_diff, diff_source)

    raw = ai_client.generate(
        system_prompt=prompt_builder.COMMIT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    title, body = validators.parse_title_body(raw)
    problems = validators.validate_commit(title, body)

    meta = {"model": args.model, "max_tokens": args.max_tokens, "temperature": args.temperature, **diff_meta}
    formatter.print_commit_result(title, body, problems, meta)
    return 1 if problems else 0


def cmd_pr(args) -> int:
    if not git_utils.is_git_repo():
        raise AiGitGenError("현재 디렉터리는 git 저장소가 아닙니다.")

    commit_log = git_utils.get_recent_commits(args.base)
    diff_text, used_base = git_utils.get_diff_for_pr(args.base)

    if not diff_text.strip() and not commit_log.strip():
        raise AiGitGenError(f"'{args.base}' 대비 비교할 변경 사항이 없습니다.")

    sendable_diff, diff_meta = _prepare_diff_for_sending(diff_text, args)
    user_prompt = prompt_builder.build_pr_user_prompt(commit_log, sendable_diff, used_base)

    raw = ai_client.generate(
        system_prompt=prompt_builder.PR_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )

    title, body = validators.parse_title_body(raw)
    problems = validators.validate_pr(title, body)

    meta = {"model": args.model, "max_tokens": args.max_tokens, "temperature": args.temperature, **diff_meta}
    formatter.print_pr_result(title, body, problems, meta)
    return 1 if problems else 0


def run(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "commit":
            return cmd_commit(args)
        if args.command == "pr":
            return cmd_pr(args)
        parser.print_help()
        return 2
    except AiGitGenError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
