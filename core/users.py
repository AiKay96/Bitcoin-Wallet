from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core.transactions import Transaction
from core.wallets import Wallet


@dataclass
class User:
    username: str
    password: str

    API_key: UUID = field(default_factory=uuid4)
    wallets: dict[UUID, Wallet] = field(default_factory=dict)
    wallets_number: int = 0
    transactions: list[Transaction] = field(default_factory=list)


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        pass

    def get(self, key: UUID) -> User:
        pass


@dataclass
class UserService:
    users: UserRepository
