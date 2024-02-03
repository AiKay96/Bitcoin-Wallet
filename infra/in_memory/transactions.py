from dataclasses import dataclass, field
from uuid import UUID

from core.errors import ExistsError, DoesNotExistError
from core.transactions import Transaction
from core.users import User


@dataclass
class TransactionInMemory:

    def create(self, transaction: Transaction) -> None:
        pass

