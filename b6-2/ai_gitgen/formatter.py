"""터미널 출력 포맷팅."""

SEP = "=" * 60


def print_commit_result(title: str, body: str, problems: list, meta: dict):
    print(SEP)
    print("커밋 메시지 초안")
    print(SEP)
    print(f"[제목] ({len(title)}자)")
    print(title)
    if body:
        print()
        print("[본문]")
        print(body)
    print()
    _print_meta(meta)
    _print_validation(problems)


def print_pr_result(title: str, body: str, problems: list, meta: dict):
    print(SEP)
    print("PR 초안")
    print(SEP)
    print(f"[제목] ({len(title)}자)")
    print(title)
    print()
    print("[본문]")
    print(body)
    print()
    _print_meta(meta)
    _print_validation(problems)


def _print_meta(meta: dict):
    print("-" * 60)
    print(f"모델: {meta.get('model')}  |  max_tokens: {meta.get('max_tokens')}"
          f"  |  temperature: {meta.get('temperature', '(기본값)')}")
    if meta.get("safe_mode"):
        masked = meta.get("masked_kinds") or []
        masked_desc = ", ".join(masked) if masked else "없음"
        trunc_desc = (
            f"{meta.get('sent_lines')}/{meta.get('total_lines')}줄 전송 (잘림)"
            if meta.get("truncated")
            else f"{meta.get('total_lines')}줄 전체 전송"
        )
        print(f"safe-mode: ON  |  마스킹된 패턴: {masked_desc}  |  diff 크기: {trunc_desc}")
    else:
        print("safe-mode: OFF")
    print("-" * 60)


def _print_validation(problems: list):
    if problems:
        print("⚠ 검증 실패 항목:")
        for p in problems:
            print(f"  - {p}")
    else:
        print("✓ 길이/형식 검증 통과")
    print(SEP)
