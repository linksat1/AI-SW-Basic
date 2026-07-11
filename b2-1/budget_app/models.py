"""데이터 모델 정의 (Transaction 등)."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

ALLOWED_TYPES = ("income", "expense")


@dataclass
class Transaction:
    """거래 내역 1건을 표현하는 데이터 모델."""

    id: str
    date: str  # YYYY-MM-DD
    type: str  # income | expense
    category: str
    amount: int  # 양수
    memo: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Transaction":
        return Transaction(
            id=data["id"],
            date=data["date"],
            type=data["type"],
            category=data["category"],
            amount=int(data["amount"]),
            memo=data.get("memo", ""),
            tags=list(data.get("tags", [])),
        )

    def to_line(self) -> str:
        """list/search 출력용 한 줄 표현."""
        tag_str = ",".join(self.tags)
        return (
            f"{self.id} | {self.date} | {self.type:<7} | {self.category} | "
            f"{self.amount} | {self.memo}" + (f" | #{tag_str}" if tag_str else "")
        )
