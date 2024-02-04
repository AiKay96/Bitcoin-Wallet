from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core import constants
from core.transactions import Transaction


@dataclass
class Wallet:
    API_key: UUID

    balance: float = 1 * constants.BTC_TO_SATOSHI
    transactions: list[Transaction] = field(default_factory=list)
    address: UUID = field(default_factory=uuid4)

    def balance_in_btc(self) -> float:
        return self.balance / constants.BTC_TO_SATOSHI


class WalletRepository(Protocol):
    def create(self, wallet: Wallet) -> Wallet:
        pass

    def get(self, key: UUID) -> Wallet:
        pass


@dataclass
class WalletService:
    wallets: WalletRepository
