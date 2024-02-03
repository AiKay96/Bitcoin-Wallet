from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import ExistsError, EqualityError, BalanceError
from core.transactions import Transaction
from infra.wallet_api.dependables import TransactionRepositoryDependable, UserRepositoryDependable, \
    WalletRepositoryDependable

transaction_api = APIRouter(tags=["Transactions"])


def extract_transaction_fields(transaction: Transaction) -> dict:
    return {
        "API_key": transaction.API_key,
        "transactionname": transaction.transactionname,
        "password": transaction.password
    }


class CreateTransactionRequest(BaseModel):
    API_key: UUID
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshis: int


class EmptyItem(BaseModel):
    pass


class DoesNotExistsError:
    pass


@transaction_api.post(
    "/transactions",
    status_code=201,
    response_model=EmptyItem,
)
def create_transaction(
        request: CreateTransactionRequest,
        transactions: TransactionRepositoryDependable,
        wallets: WalletRepositoryDependable,
        users: UserRepositoryDependable
) -> dict[str, dict] | JSONResponse:
    try:
        transaction = Transaction(
            wallet_from=request.wallet_from,
            wallet_to=request.wallet_to,
            amount=request.amount_in_satoshis,
        )
        user_from = users.get(request.API_key)
        user_to = users.get(wallets.get(request.wallet_to).API_key)
        transactions.create(transaction, user_from, user_to)
        return {}
    except DoesNotExistsError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Wallet does not exist."},
        )
    except EqualityError:
        return JSONResponse(
            status_code=400,
            content={"message": f"Transaction within the same wallet is not allowed."},
        )
    except BalanceError:
        return JSONResponse(
            status_code=400,
            content={"message": f"Not enough balance to complete the transaction."},
        )
