from dataclasses import dataclass
from core.transactions import Transaction


@dataclass
class TransactionInMemory:

    def create(self, transaction: Transaction) -> None:
        pass
