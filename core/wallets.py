from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core.transactions import Transaction


@dataclass
class Wallet:
    API_key: UUID

    balance: float = 1.0
    transactions: list[Transaction] = field(default_factory=list)
    address: UUID = field(default_factory=uuid4)

    def balance_in_usd(self) -> float:
        return self.balance * 2


class WalletRepository(Protocol):
    def create(self, wallet: Wallet) -> Wallet:
        pass

    def get(self, key: UUID) -> Wallet:
        pass


@dataclass
class WalletService:
    wallets: WalletRepository
