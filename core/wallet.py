from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from core import transaction


@dataclass
class Wallet:
    address: UUID
    API_key: UUID
    balance: float
    transactions: list[transaction]


class WalletRepository(Protocol):
    pass


@dataclass
class WalletService:
    wallets: WalletRepository
