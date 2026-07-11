"""파일 입출력(저장소) 계층.

- JSONL(줄 단위 JSON) 형식으로 transactions / categories / budgets 3개 파일에
  각각 영구 저장한다.
- 조회는 제너레이터(yield)로 한 줄씩 읽어 스트리밍 처리한다.
- 수정/삭제는 임시 파일에 새 내용을 쓴 뒤 os.replace로 원자적으로 교체한다.
"""
from __future__ import annotations

import json
import os
from collections import deque
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

from budget_app.models import Transaction


def _read_jsonl(path: Path) -> Iterator[dict]:
    """파일이 없으면 빈 이터레이터, 있으면 한 줄씩 JSON으로 파싱해 yield."""
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _atomic_write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    """임시 파일에 먼저 쓰고 os.replace로 교체해 쓰다가 중단돼도 원본이 깨지지 않게 한다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp_path, path)


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


class TransactionRepository:
    """transactions.jsonl 파일 하나를 담당하는 저장소."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def iter_all(self) -> Iterator[Transaction]:
        """파일을 한 줄씩 읽어 Transaction으로 변환해 yield (스트리밍)."""
        for row in _read_jsonl(self.path):
            yield Transaction.from_dict(row)

    def next_id(self) -> str:
        max_no = 0
        for tx in self.iter_all():
            try:
                no = int(tx.id.split("-")[-1])
                max_no = max(max_no, no)
            except ValueError:
                continue
        return f"TX-{max_no + 1:06d}"

    def add(self, tx: Transaction) -> None:
        _append_jsonl(self.path, tx.to_dict())

    def find(self, tx_id: str) -> Transaction | None:
        for tx in self.iter_all():
            if tx.id == tx_id:
                return tx
        return None

    def latest(self, limit: int) -> Iterator[Transaction]:
        """파일 전체를 리스트로 만들지 않고, 최근 limit개만 deque로 유지하며
        한 줄씩 읽는 방식으로 최신 limit건을 구한다(스트리밍 처리)."""
        window: deque[Transaction] = deque(maxlen=limit)
        for tx in self.iter_all():
            window.append(tx)
        yield from reversed(window)

    def search(self, predicate: Callable[[Transaction], bool]) -> Iterator[Transaction]:
        """조건(predicate)에 맞는 거래만 최신순으로 yield.

        한 줄씩 읽으면서 조건에 맞는 것만 골라내므로(제너레이터),
        조건에 맞지 않는 대다수 데이터는 Transaction 객체로 남겨두지 않는다.
        최신순 정렬을 위해 '조건에 맞는 결과'만 모아서 뒤집는다.
        """
        matched = [tx for tx in self.iter_all() if predicate(tx)]
        yield from reversed(matched)

    def update(self, tx_id: str, apply_changes: Callable[[Transaction], Transaction]) -> bool:
        found = False
        rows: list[dict] = []
        for tx in self.iter_all():
            if tx.id == tx_id:
                tx = apply_changes(tx)
                found = True
            rows.append(tx.to_dict())
        if found:
            _atomic_write_jsonl(self.path, rows)
        return found

    def delete(self, tx_id: str) -> bool:
        found = False
        rows: list[dict] = []
        for tx in self.iter_all():
            if tx.id == tx_id:
                found = True
                continue
            rows.append(tx.to_dict())
        if found:
            _atomic_write_jsonl(self.path, rows)
        return found

    def used_categories(self) -> set[str]:
        return {tx.category for tx in self.iter_all()}


class CategoryStore:
    """categories.jsonl 파일 하나를 담당하는 저장소."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self) -> list[str]:
        return [row["name"] for row in _read_jsonl(self.path)]

    def exists(self, name: str) -> bool:
        return name in self.list()

    def ensure_default(self, defaults: list[str]) -> None:
        if not self.path.exists() or self.path.stat().st_size == 0:
            _atomic_write_jsonl(self.path, [{"name": name} for name in defaults])

    def add(self, name: str) -> bool:
        names = self.list()
        if name in names:
            return False
        names.append(name)
        _atomic_write_jsonl(self.path, [{"name": n} for n in names])
        return True

    def remove(self, name: str) -> bool:
        names = self.list()
        if name not in names:
            return False
        names.remove(name)
        _atomic_write_jsonl(self.path, [{"name": n} for n in names])
        return True


class BudgetStore:
    """budgets.jsonl 파일 하나를 담당하는 저장소 (월별 예산 금액)."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def _all(self) -> dict[str, int]:
        return {row["month"]: int(row["amount"]) for row in _read_jsonl(self.path)}

    def get(self, month: str) -> int | None:
        return self._all().get(month)

    def set(self, month: str, amount: int) -> None:
        budgets = self._all()
        budgets[month] = amount
        rows = [{"month": m, "amount": a} for m, a in sorted(budgets.items())]
        _atomic_write_jsonl(self.path, rows)
