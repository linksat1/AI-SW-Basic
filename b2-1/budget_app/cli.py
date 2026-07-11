"""CLI 계층: 인자 파싱, 대화형 입력, 화면 출력만 담당한다.

실제 검증/저장 로직은 service.py / repository.py에 위임한다.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from budget_app.decorators import handle_errors, log_execution
from budget_app.errors import AppError
from budget_app.repository import BudgetStore, CategoryStore, TransactionRepository
from budget_app.service import BudgetService


def _build_service(data_dir: str) -> BudgetService:
    base = Path(data_dir)
    tx_repo = TransactionRepository(base / "transactions.jsonl")
    cat_store = CategoryStore(base / "categories.jsonl")
    budget_store = BudgetStore(base / "budgets.jsonl")
    return BudgetService(tx_repo, cat_store, budget_store)


def _prompt_until_valid(prompt: str, validate) -> str:
    """유효할 때까지 재입력을 요구하는 공용 헬퍼."""
    while True:
        value = input(prompt)
        try:
            validate(value)
            return value
        except AppError as e:
            print(f"[오류] {e.message}")
            if e.hint:
                print(f"[힌트] {e.hint}")


# ---------------------------------------------------------------------------
# 각 명령어 구현
# ---------------------------------------------------------------------------

@handle_errors
@log_execution
def cmd_add(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    from budget_app.service import validate_amount, validate_date, validate_type

    date = _prompt_until_valid("날짜(YYYY-MM-DD): ", validate_date)
    type_ = _prompt_until_valid("타입(income/expense): ", validate_type)

    while True:
        category = input("카테고리: ")
        try:
            service._validate_category_exists(category)
            break
        except AppError as e:
            print(f"[오류] {e.message}")
            if e.hint:
                print(f"[힌트] {e.hint}")
            print(f"등록된 카테고리: {', '.join(service.list_categories())}")

    amount = _prompt_until_valid("금액(양수): ", validate_amount)
    memo = input("메모(선택): ")
    tags = input("태그(쉼표로 구분, 없으면 엔터): ")

    tx = service.add_transaction(date, type_, category, amount, memo, tags)
    print(f"[저장 완료] id={tx.id}")
    return 0


@handle_errors
@log_execution
def cmd_list(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    rows = list(service.list_transactions(args.limit))
    if not rows:
        print("[안내] 저장된 거래가 없습니다.")
        return 0
    for tx in rows:
        print(tx.to_line())
    return 0


@handle_errors
@log_execution
def cmd_search(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    rows = list(
        service.search_transactions(
            date_from=args.from_,
            date_to=args.to,
            category=args.category,
            type_=args.type,
            query=args.q,
            tag=args.tag,
        )
    )
    if not rows:
        print("[안내] 조건에 맞는 거래가 없습니다.")
        return 0
    for tx in rows:
        print(tx.to_line())
    return 0


@handle_errors
@log_execution
def cmd_summary(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    result = service.summary(args.month, args.top)

    if not result["found_any"]:
        print(f"[안내] {args.month} 데이터 없음")
        return 0

    print(f"총 수입: {result['income']}원")
    print(f"총 지출: {result['expense']}원")
    print(f"잔액: {result['balance']}원")

    if result["budget"] is not None:
        print(f"예산: {result['budget']}원 (사용률 {result['usage_percent']}%)")
        if result["over_budget"]:
            print("[경고] 이번 달 예산을 초과했습니다.")

    if result["top_categories"]:
        print()
        print(f"지출 TOP {args.top}")
        for i, (category, amount) in enumerate(result["top_categories"], start=1):
            print(f"{i}) {category} {amount}원")

    return 0


@handle_errors
@log_execution
def cmd_budget_set(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    amount = service.set_budget(args.month, args.amount)
    print(f"[저장 완료] {args.month} 예산 {amount}원")
    return 0


@handle_errors
@log_execution
def cmd_category_add(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    name = input("카테고리명: ")
    service.add_category(name)
    print(f"[저장 완료] category={name}")
    return 0


@handle_errors
@log_execution
def cmd_category_list(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    for name in service.list_categories():
        print(f"- {name}")
    return 0


@handle_errors
@log_execution
def cmd_category_remove(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    name = input("삭제할 카테고리명: ")
    service.remove_category(name)
    print(f"[삭제 완료] category={name}")
    return 0


@handle_errors
@log_execution
def cmd_update(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    tx = service.update_transaction(
        args.id,
        date=args.date,
        type_=args.type,
        category=args.category,
        amount=args.amount,
        memo=args.memo,
        tags=args.tags,
    )
    print(f"[수정 완료] id={tx.id}")
    return 0


@handle_errors
@log_execution
def cmd_delete(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    service.delete_transaction(args.id)
    print(f"[삭제 완료] id={args.id}")
    return 0


@handle_errors
@log_execution
def cmd_import(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    imported, skipped = service.import_csv(args.from_)
    print(f"[완료] imported={imported}, skipped={skipped}")
    return 0


@handle_errors
@log_execution
def cmd_export(args: argparse.Namespace) -> int:
    service = _build_service(args.data_dir)
    count = service.export_csv(args.out, month=args.month, date_from=args.from_, date_to=args.to)
    print(f"[완료] {args.out} ({count} records)")
    return 0


# ---------------------------------------------------------------------------
# argparse 구성
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--data-dir", default="data", help="데이터 저장 폴더 (기본값: ./data)"
    )

    parser = argparse.ArgumentParser(
        prog="python -m budget_app",
        description="파일 기반 가계부 콘솔 프로그램",
        parents=[common],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_add = subparsers.add_parser("add", parents=[common], help="거래 추가 (대화형)")
    p_add.set_defaults(func=cmd_add)

    p_list = subparsers.add_parser("list", parents=[common], help="거래 목록 (최신순)")
    p_list.add_argument("--limit", type=int, default=20, help="출력할 최대 건수 (기본값: 20)")
    p_list.set_defaults(func=cmd_list)

    p_search = subparsers.add_parser("search", parents=[common], help="조건 기반 거래 검색")
    p_search.add_argument("--from", dest="from_", help="검색 시작일 YYYY-MM-DD")
    p_search.add_argument("--to", help="검색 종료일 YYYY-MM-DD")
    p_search.add_argument("--category", help="카테고리")
    p_search.add_argument("--type", choices=["income", "expense"], help="income 또는 expense")
    p_search.add_argument("--q", help="메모 검색 키워드")
    p_search.add_argument("--tag", help="태그")
    p_search.set_defaults(func=cmd_search)

    p_summary = subparsers.add_parser("summary", parents=[common], help="월별 요약")
    p_summary.add_argument("--month", required=True, help="YYYY-MM")
    p_summary.add_argument("--top", type=int, default=5, help="지출 TOP N (기본값: 5)")
    p_summary.set_defaults(func=cmd_summary)

    p_budget = subparsers.add_parser("budget", parents=[common], help="예산 설정")
    budget_sub = p_budget.add_subparsers(dest="budget_command", required=True)
    p_budget_set = budget_sub.add_parser("set", parents=[common], help="월 예산 설정")
    p_budget_set.add_argument("--month", required=True, help="YYYY-MM")
    p_budget_set.add_argument("--amount", required=True, help="예산 금액(양수)")
    p_budget_set.set_defaults(func=cmd_budget_set)

    p_category = subparsers.add_parser("category", parents=[common], help="카테고리 관리")
    category_sub = p_category.add_subparsers(dest="category_command", required=True)
    p_cat_add = category_sub.add_parser("add", parents=[common], help="카테고리 추가 (대화형)")
    p_cat_add.set_defaults(func=cmd_category_add)
    p_cat_list = category_sub.add_parser("list", parents=[common], help="카테고리 목록")
    p_cat_list.set_defaults(func=cmd_category_list)
    p_cat_remove = category_sub.add_parser("remove", parents=[common], help="카테고리 삭제 (대화형)")
    p_cat_remove.set_defaults(func=cmd_category_remove)

    p_update = subparsers.add_parser("update", parents=[common], help="거래 수정 (옵션 기반)")
    p_update.add_argument("--id", required=True, help="수정할 거래 id")
    p_update.add_argument("--date", help="YYYY-MM-DD")
    p_update.add_argument("--type", choices=["income", "expense"])
    p_update.add_argument("--category", help="카테고리")
    p_update.add_argument("--amount", help="양수 금액")
    p_update.add_argument("--memo", help="메모")
    p_update.add_argument("--tags", help="쉼표로 구분된 태그")
    p_update.set_defaults(func=cmd_update)

    p_delete = subparsers.add_parser("delete", parents=[common], help="거래 삭제")
    p_delete.add_argument("--id", required=True, help="삭제할 거래 id")
    p_delete.set_defaults(func=cmd_delete)

    p_import = subparsers.add_parser("import", parents=[common], help="CSV 가져오기")
    p_import.add_argument("--from", dest="from_", required=True, help="가져올 CSV 파일 경로")
    p_import.set_defaults(func=cmd_import)

    p_export = subparsers.add_parser("export", parents=[common], help="CSV 내보내기")
    p_export.add_argument("--out", required=True, help="내보낼 CSV 파일 경로")
    p_export.add_argument("--month", help="YYYY-MM")
    p_export.add_argument("--from", dest="from_", help="YYYY-MM-DD")
    p_export.add_argument("--to", help="YYYY-MM-DD")
    p_export.set_defaults(func=cmd_export)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
