from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from core import wallet, transaction


@dataclass
class User:
    username: str
    password: str

    API_key: UUID = field(default_factory=uuid4)
    wallets: list[wallet] = field(default_factory=list)
    wallets_number: int = 0
    transactions: list[transaction] = field(default_factory=list)


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        pass


@dataclass
class UserService:
    users: UserRepository
