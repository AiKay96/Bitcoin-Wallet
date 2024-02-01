from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from src import wallet, transaction


@dataclass
class User:
    API_key: UUID
    username: str
    password: str
    wallets: list[wallet]
    wallets_number: int
    transactions: list[transaction]


class UserRepository(Protocol):
    pass


@dataclass
class UserService:
    users: UserRepository
