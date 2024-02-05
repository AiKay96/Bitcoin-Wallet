from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Transaction:
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshis: float
    transaction_id: UUID = field(default_factory=uuid4)

    def __eq__(self, other) -> bool:
        return self.transaction_id == other.transaction_id


class TransactionRepository(Protocol):
    pass


@dataclass
class TransactionService:
    transactions: TransactionRepository
