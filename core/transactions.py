from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4




@dataclass
class Transaction:
    wallet_from: UUID
    wallet_to: UUID
    amount: float


class TransactionRepository(Protocol):
    pass


@dataclass
class TransactionService:
    transactions: TransactionRepository





