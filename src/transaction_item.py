from dataclasses import dataclass
from datetime import date


@dataclass
class TransactionItem:
    name: str
    date: date
    amount: float
    description: str
