"""비즈니스 로직(검증 + 규칙)을 담당하는 서비스 계층.

CLI는 사용자 입력을 받아 이 계층의 메서드만 호출하고,
파일을 어떻게 읽고 쓰는지는 repository 계층에 위임한다.
"""
from __future__ import annotations

import csv
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from budget_app.errors import AppError
from budget_app.models import ALLOWED_TYPES, Transaction
from budget_app.repository import BudgetStore, CategoryStore, TransactionRepository

DEFAULT_CATEGORIES = ["food", "transport", "rent", "salary", "etc"]
CSV_FIELDS = ["date", "type", "category", "amount", "memo", "tags"]


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise AppError(
            "날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).",
            hint="예: 2024-01-15",
        )
    return date_str


def validate_month(month_str: str) -> str:
    try:
        datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        raise AppError(
            "월 형식이 올바르지 않습니다 (YYYY-MM).",
            hint="예: 2024-01",
        )
    return month_str


def validate_type(type_str: str) -> str:
    if type_str not in ALLOWED_TYPES:
        raise AppError(
            f"type은 {'/'.join(ALLOWED_TYPES)} 중 하나여야 합니다.",
            hint="예: expense",
        )
    return type_str


def validate_amount(amount_str: str) -> int:
    try:
        amount = int(amount_str)
    except ValueError:
        raise AppError("금액은 숫자여야 합니다.", hint="예: 15000")
    if amount <= 0:
        raise AppError("금액은 0보다 큰 양수여야 합니다.", hint="예: 15000")
    return amount


def parse_tags(tags_str: str) -> list[str]:
    if not tags_str:
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]


class BudgetService:
    def __init__(
        self,
        tx_repo: TransactionRepository,
        cat_store: CategoryStore,
        budget_store: BudgetStore,
    ) -> None:
        self.tx_repo = tx_repo
        self.cat_store = cat_store
        self.budget_store = budget_store
        self.cat_store.ensure_default(DEFAULT_CATEGORIES)

    # ---------- 카테고리 ----------
    def list_categories(self) -> list[str]:
        return self.cat_store.list()

    def add_category(self, name: str) -> None:
        if not self.cat_store.add(name):
            raise AppError(f"이미 존재하는 카테고리입니다: {name}")

    def remove_category(self, name: str) -> None:
        if not self.cat_store.exists(name):
            raise AppError(f"존재하지 않는 카테고리입니다: {name}")
        if name in self.tx_repo.used_categories():
            raise AppError(
                f"'{name}' 카테고리를 사용 중인 거래가 있어 삭제할 수 없습니다.",
                hint="해당 카테고리를 사용하는 거래를 먼저 다른 카테고리로 옮기거나 삭제하세요.",
            )
        self.cat_store.remove(name)

    def _validate_category_exists(self, category: str) -> None:
        if not self.cat_store.exists(category):
            raise AppError(
                f"등록되지 않은 카테고리입니다: {category}",
                hint="`category add`로 먼저 등록하거나 `category list`로 목록을 확인하세요.",
            )

    # ---------- 거래 ----------
    def add_transaction(
        self,
        date: str,
        type_: str,
        category: str,
        amount: str,
        memo: str = "",
        tags: str = "",
    ) -> Transaction:
        date = validate_date(date)
        type_ = validate_type(type_)
        amount_int = validate_amount(amount)
        self._validate_category_exists(category)
        tx = Transaction(
            id=self.tx_repo.next_id(),
            date=date,
            type=type_,
            category=category,
            amount=amount_int,
            memo=memo,
            tags=parse_tags(tags),
        )
        self.tx_repo.add(tx)
        return tx

    def list_transactions(self, limit: int) -> Iterator[Transaction]:
        return self.tx_repo.latest(limit)

    def search_transactions(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        category: str | None = None,
        type_: str | None = None,
        query: str | None = None,
        tag: str | None = None,
    ) -> Iterator[Transaction]:
        if date_from:
            validate_date(date_from)
        if date_to:
            validate_date(date_to)

        def predicate(tx: Transaction) -> bool:
            if date_from and tx.date < date_from:
                return False
            if date_to and tx.date > date_to:
                return False
            if category and tx.category != category:
                return False
            if type_ and tx.type != type_:
                return False
            if query and query not in tx.memo:
                return False
            if tag and tag not in tx.tags:
                return False
            return True

        return self.tx_repo.search(predicate)

    def update_transaction(
        self,
        tx_id: str,
        date: str | None = None,
        type_: str | None = None,
        category: str | None = None,
        amount: str | None = None,
        memo: str | None = None,
        tags: str | None = None,
    ) -> Transaction:
        if date is not None:
            validate_date(date)
        if type_ is not None:
            validate_type(type_)
        if amount is not None:
            validate_amount(amount)
        if category is not None:
            self._validate_category_exists(category)

        updated_holder: dict[str, Transaction] = {}

        def apply_changes(tx: Transaction) -> Transaction:
            if date is not None:
                tx.date = date
            if type_ is not None:
                tx.type = type_
            if category is not None:
                tx.category = category
            if amount is not None:
                tx.amount = validate_amount(amount)
            if memo is not None:
                tx.memo = memo
            if tags is not None:
                tx.tags = parse_tags(tags)
            updated_holder["tx"] = tx
            return tx

        found = self.tx_repo.update(tx_id, apply_changes)
        if not found:
            raise AppError(
                f"존재하지 않는 거래 id입니다: {tx_id}",
                hint="`list` 명령으로 올바른 id를 확인하세요.",
            )
        return updated_holder["tx"]

    def delete_transaction(self, tx_id: str) -> None:
        if not self.tx_repo.delete(tx_id):
            raise AppError(
                f"존재하지 않는 거래 id입니다: {tx_id}",
                hint="`list` 명령으로 올바른 id를 확인하세요.",
            )

    # ---------- 예산 / 요약 ----------
    def set_budget(self, month: str, amount: str) -> int:
        validate_month(month)
        amount_int = validate_amount(amount)
        self.budget_store.set(month, amount_int)
        return amount_int

    def summary(self, month: str, top: int) -> dict:
        validate_month(month)
        income = 0
        expense = 0
        category_expense: dict[str, int] = {}
        found_any = False
        for tx in self.tx_repo.iter_all():
            if not tx.date.startswith(month):
                continue
            found_any = True
            if tx.type == "income":
                income += tx.amount
            else:
                expense += tx.amount
                category_expense[tx.category] = category_expense.get(tx.category, 0) + tx.amount

        top_categories = sorted(category_expense.items(), key=lambda kv: kv[1], reverse=True)[:top]
        budget = self.budget_store.get(month)
        usage_percent = None
        over_budget = False
        if budget is not None and budget > 0:
            usage_percent = round(expense / budget * 100, 1)
            over_budget = expense > budget

        return {
            "month": month,
            "found_any": found_any,
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "top_categories": top_categories,
            "budget": budget,
            "usage_percent": usage_percent,
            "over_budget": over_budget,
        }

    # ---------- import / export ----------
    def import_csv(self, path: str) -> tuple[int, int]:
        csv_path = Path(path)
        if not csv_path.exists():
            raise AppError(f"파일을 찾을 수 없습니다: {path}")

        imported = 0
        skipped = 0
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.add_transaction(
                        date=row["date"],
                        type_=row["type"],
                        category=row["category"],
                        amount=row["amount"],
                        memo=row.get("memo", "") or "",
                        tags=row.get("tags", "") or "",
                    )
                    imported += 1
                except (AppError, KeyError):
                    skipped += 1
        return imported, skipped

    def export_csv(
        self,
        out_path: str,
        month: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> int:
        if not month and not date_from and not date_to:
            raise AppError(
                "export는 --month 또는 --from/--to 조건이 최소 1개 필요합니다.",
                hint="예: export --out export.csv --month 2024-01",
            )

        def predicate(tx: Transaction) -> bool:
            if month and not tx.date.startswith(month):
                return False
            if date_from and tx.date < date_from:
                return False
            if date_to and tx.date > date_to:
                return False
            return True

        rows = [tx for tx in self.tx_repo.iter_all() if predicate(tx)]
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for tx in rows:
                writer.writerow(
                    {
                        "date": tx.date,
                        "type": tx.type,
                        "category": tx.category,
                        "amount": tx.amount,
                        "memo": tx.memo,
                        "tags": ",".join(tx.tags),
                    }
                )
        return len(rows)
