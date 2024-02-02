from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core import transaction


@dataclass
class Wallet:
    API_key: UUID

    balance: float = 1.0
    transactions: list[transaction] = field(default_factory=list)
    address: UUID = field(default_factory=uuid4)

    def balance_in_usd(self) -> float:
        return self.balance * 2


class WalletRepository(Protocol):
    pass


@dataclass
class WalletService:
    wallets: WalletRepository
