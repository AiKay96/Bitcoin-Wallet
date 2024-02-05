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
        return (self.wallet_from == other.wallet_from
                and self.wallet_to == other.wallet_to
                and self.amount_in_satoshis == other.amount_in_satoshis
                and self.transaction_id == other.transaction_id)


class TransactionRepository(Protocol):
    pass


@dataclass
class TransactionService:
    transactions: TransactionRepository
