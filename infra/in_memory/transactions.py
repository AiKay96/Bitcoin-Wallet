import uuid
from dataclasses import dataclass

from core.errors import DoesNotExistError, EqualityError, BalanceError
from core.transactions import Transaction
from core.users import User


@dataclass
class TransactionInMemory:

    def create(self, transaction: Transaction, user_from: User, user_to: User) -> None:
        wallet_from = user_from.wallets[transaction.wallet_from]
        wallet_to = user_to.wallets[transaction.wallet_to]

        if wallet_from is None or wallet_to is None:
            raise DoesNotExistError("wallet does not exists.")

        if transaction.wallet_from == transaction.wallet_to:
            raise EqualityError("Can not send money on the same wallet.")

        if wallet_from.balance < transaction.amount:
            raise BalanceError("Not enough money.")

        wallet_from.balance -= transaction.amount
        wallet_to.balance += transaction.amount

        wallet_from.transactions.append(transaction)
        wallet_to.transactions.append(transaction)

        user_from.transactions.append(transaction)
        user_to.transactions.append(transaction)

        pass
