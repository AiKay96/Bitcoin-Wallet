import uuid
from dataclasses import dataclass
from core.transactions import Transaction
from core.users import User


@dataclass
class TransactionInMemory:

    def create(self, transaction: Transaction, user_from: User, user_to: User) -> None:
        pass
