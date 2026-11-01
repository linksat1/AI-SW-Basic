"""CLI 엔트리포인트: describe 명령의 전체 흐름을 조립한다.

흐름: Git 수집 -> 수정 의도 입력 -> (safe-mode) -> 프롬프트 -> AI 호출(최대 2회)
      -> 파싱/정리 -> 검증 -> (필요 시 재생성 1회 -> 후처리 보정) -> 출력
"""

import argparse
import os
import sys

from . import ai_client, generator
from .convention import load_convention
from .git_context import GitError, collect_git_context
from .safe_mode import apply_safe_mode, validate_patterns

MAX_API_CALLS = 2
LARGE_DIFF_LINES = 2000
BAR_LONG = "=" * 60


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="main.py", description="AI 기반 코드 설명 자동 생성기")
    parser.add_argument("--version", action="version", version=f"%(prog)s {generator.VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    d = subparsers.add_parser("describe", help="Git 변경 사항을 기반으로 코드 설명을 생성합니다.")
    d.add_argument("--intent", "-i", default=None, help="수정 의도/요약 (생략하면 대화식으로 입력)")
    d.add_argument("--no-input", action="store_true", help="대화식 입력을 건너뜁니다.")
    g = d.add_argument_group("AI API 파라미터")
    g.add_argument("--model", default=ai_client.DEFAULT_MODEL, help=f"모델 ID (기본: {ai_client.DEFAULT_MODEL})")
    g.add_argument("--max-tokens", type=int, default=ai_client.DEFAULT_MAX_TOKENS,
                   help=f"최대 출력 토큰, 사고 토큰 포함 (기본: {ai_client.DEFAULT_MAX_TOKENS})")
    g.add_argument("--effort", choices=ai_client.EFFORT_LEVELS, default=ai_client.DEFAULT_EFFORT,
                   help=f"추론 노력 수준 (기본: {ai_client.DEFAULT_EFFORT})")
    g.add_argument("--temperature", type=float, default=None,
                   help="샘플링 온도 (기본: 미전송. 현재 API 버전/기본 모델은 지원하지 않음)")
    s = d.add_argument_group("safe-mode / 컨벤션")
    s.add_argument("--safe-mode", action="store_true", help="민감정보 마스킹 + diff 전송량 제한")
    s.add_argument("--max-files", type=int, default=None, help="safe-mode 전송 최대 파일 수 (기본 10)")
    s.add_argument("--max-diff-lines", type=int, default=None, help="safe-mode 전송 최대 diff 줄 수 (기본 200)")
    s.add_argument("--mask-pattern", action="append", default=[], metavar="REGEX",
                   help="safe-mode 추가 마스킹 정규표현식 (여러 번 지정 가능)")
    s.add_argument("--convention", default=None, metavar="PATH",
                   help="컨벤션 JSON 경로 (기본: 저장소 루트의 .ai-code-summary.json)")
    x = d.add_argument_group("실행 모드")
    x.add_argument("--mock", action="store_true", help="API 호출 없이 데모 응답으로 흐름을 확인합니다.")
    x.add_argument("--dry-run", action="store_true", help="AI로 보낼 프롬프트만 출력하고 종료합니다.")
    return parser


def _positive(value, name):
    if value is not None and value <= 0:
        raise ValueError(f"{name}는 1 이상이어야 합니다.")


def read_intent(args) -> str:
    """수정 의도를 옵션 또는 대화식 입력으로 받는다."""
    if args.intent is not None:
        return args.intent.strip()
    if args.no_input or not sys.stdin.isatty():
        return ""
    try:
        return input("수정 의도를 입력하세요 (Enter: 건너뛰기)> ").strip()
    except EOFError:
        return ""


def describe_command(args) -> int:
    try:
        _positive(args.max_tokens, "--max-tokens")
        _positive(args.max_files, "--max-files")
        _positive(args.max_diff_lines, "--max-diff-lines")
        validate_patterns(args.mask_pattern)
        ctx = collect_git_context(os.getcwd())
        convention = load_convention(ctx.root, args.convention)
    except (GitError, ValueError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if not ctx.has_changes:
        print("[INFO] 변경 사항이 없습니다. 코드 설명을 생성하지 않고 종료합니다.")
        return 0
    if not (args.mock or args.dry_run):
        try:
            ai_client.ensure_ready()
        except ai_client.AIError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 1
    print(f"[INFO] Git status 수집 완료: {len(ctx.files)}개 파일 변경 감지")
    print(f"[INFO] Git diff 수집 완료: {ctx.diff_line_count}줄")
    print(f"[INFO] 컨벤션: {convention.name} ({convention.source})")

    intent = read_intent(args)
    print(f"[INFO] 사용자 입력 수집 완료: {'수정 의도 ' + str(len(intent)) + '자' if intent else '입력 없음'}")

    diff_text = ctx.diff_text
    footer = []
    if args.safe_mode:
        policy = convention.safe_mode
        if args.max_files is not None:
            policy.max_files = args.max_files
        if args.max_diff_lines is not None:
            policy.max_lines = args.max_diff_lines
        policy.extra_patterns += args.mask_pattern
        result = apply_safe_mode(diff_text, policy)
        diff_text = result.text
        print(f"[INFO] safe-mode ON: {result.summary()}")
        footer.append(f"[INFO] safe-mode ON | {result.summary()}")
    else:
        print("[INFO] safe-mode OFF: diff 전체를 전송합니다.")
        footer.append("[INFO] safe-mode OFF")
        if ctx.diff_line_count > LARGE_DIFF_LINES:
            print(f"[WARN] diff가 {ctx.diff_line_count}줄입니다. 비용/민감정보를 줄이려면 --safe-mode를 권장합니다.")

    prompt = generator.build_user_prompt(ctx.status_text, ctx.files, diff_text, intent, convention)
    if args.dry_run:
        print("[INFO] dry-run: AI API를 호출하지 않습니다. 전송될 프롬프트는 아래와 같습니다.")
        print(BAR_LONG)
        print(prompt)
        print(BAR_LONG)
        return 0

    settings = ai_client.ModelSettings(args.model, args.max_tokens, args.effort, args.temperature)
    calls = 0
    try:
        desc, report = None, None
        feedback = None
        while calls < MAX_API_CALLS:
            calls += 1
            if args.mock:
                print(f"[INFO] mock 모드: AI API 대신 데모 응답 사용 ({calls}회차)")
                raw = generator.generate_mock_response(ctx.files, intent, convention)
            else:
                print(f"[INFO] AI API 요청 중... (model={settings.model}, effort={settings.effort}, "
                      f"max_tokens={settings.max_tokens}, {calls}회차)")
                user_prompt = prompt if feedback is None else generator.build_user_prompt(
                    ctx.status_text, ctx.files, diff_text, intent, convention, feedback)
                raw = ai_client.call_model(generator.SYSTEM_PROMPT, user_prompt, settings)
            desc = generator.normalize(generator.parse_title_body(raw))
            report = generator.validate(desc, convention)
            if report.ok:
                break
            print(f"[WARN] 형식 검증 실패 {len(report.errors)}건: " + " / ".join(report.errors))
            feedback = report.errors
            if args.mock:
                break  # mock 응답은 같은 결과이므로 재생성하지 않는다.
            if calls < MAX_API_CALLS:
                print("[INFO] 검증 오류를 피드백으로 넣어 1회 재생성합니다.")
    except ai_client.AIError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        print(f"[INFO] AI API 호출 횟수: {0 if args.mock else calls}회", file=sys.stderr)
        return 1

    if not report.ok:
        print("[INFO] 남은 형식 오류를 후처리로 보정합니다.")
        desc = generator.repair(desc, convention)
        report = generator.validate(desc, convention)

    api_calls = 0 if args.mock else calls
    print("[DONE] 코드 설명 생성 완료")
    print()
    footer.append(f"[INFO] AI API 호출 횟수: {api_calls}회 (최대 {MAX_API_CALLS}회)")
    print(generator.render(desc, report, footer))
    return 0 if report.ok else 1



def main(argv=None) -> int:
    # 파이프로 출력할 때도 stdout/stderr 순서가 섞이지 않도록 줄 단위로 내보낸다.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(line_buffering=True)
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "describe":
        return describe_command(args)
    parser.print_help()
    return 2
