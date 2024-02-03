from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass
class Transaction:
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshis: float


class TransactionRepository(Protocol):
    pass


@dataclass
class TransactionService:
    transactions: TransactionRepository
