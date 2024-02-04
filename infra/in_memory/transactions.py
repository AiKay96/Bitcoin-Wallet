from dataclasses import dataclass

from core import constants
from core.errors import DoesNotExistError, EqualityError, BalanceError
from core.transactions import Transaction
from core.users import User


@dataclass
class TransactionInMemory:

    @staticmethod
    def create(transaction: Transaction, user_from: User, user_to: User) -> int:
        wallet_from = user_from.wallets[transaction.wallet_from]
        wallet_to = user_to.wallets[transaction.wallet_to]

        if wallet_from is None or wallet_to is None:
            raise DoesNotExistError("wallet does not exists.")

        if transaction.wallet_from == transaction.wallet_to:
            raise EqualityError("Can not send money on the same wallet.")

        if wallet_from.balance < transaction.amount_in_satoshis:
            raise BalanceError("Not enough money.")

        wallet_from.balance -= transaction.amount_in_satoshis
        wallet_to.balance += transaction.amount_in_satoshis * (1-constants.COMMISSION)

        wallet_from.transactions.append(transaction)
        wallet_to.transactions.append(transaction)

        user_from.transactions.append(transaction)
        user_to.transactions.append(transaction)

        commission = (
            round(transaction.amount_in_satoshis * constants.COMMISSION)
            if wallet_from.API_key != wallet_to.API_key
            else 0
        )
        return commission
