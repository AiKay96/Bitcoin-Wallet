import requests
from uuid import UUID

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import DoesNotExistError, CapacityError
from core.wallets import Wallet
from infra.wallet_api.dependables import WalletRepositoryDependable, UserRepositoryDependable

wallet_api = APIRouter(tags=["Wallets"])


def usd_rate():
    response = requests.get('https://blockchain.info/ticker')
    data = response.json()
    return data['USD']['last']


def extract_wallet_fields(wallet: Wallet) -> dict:
    return {
        "address": wallet.address,
        "balance_in_BTC": wallet.balance_in_btc(),
        "balance_in_USD": wallet.balance_in_btc() * usd_rate()
    }


class CreateWalletRequest(BaseModel):
    API_key: UUID


class WalletItem(BaseModel):
    address: UUID
    balance_in_BTC: float
    balance_in_USD: float


class WalletItemEnvelope(BaseModel):
    wallet: WalletItem


class TransactionItem(BaseModel):
    wallet_from: UUID
    wallet_to: UUID
    amount_in_satoshis: int


class TransactionItemEnvelope(BaseModel):
    transaction: TransactionItem


class TransactionListEnvelope(BaseModel):
    transactions: list[TransactionItem]


@wallet_api.post(
    "/wallets",
    status_code=201,
    response_model=WalletItemEnvelope,
)
def create_wallet(
        request: CreateWalletRequest,
        wallets: WalletRepositoryDependable,
        users: UserRepositoryDependable,
) -> dict[str, dict] | JSONResponse:
    try:
        wallet = Wallet(**request.model_dump())
        user = users.get(request.API_key)
        wallets.create(wallet, user)

        response_data = extract_wallet_fields(wallet)

        return {"wallet": response_data}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": f"User does not exists."},
        )
    except CapacityError:
        return JSONResponse(
            status_code=403,
            content={"message": f"User has reached the maximum capacity of wallets."},
        )


@wallet_api.get(
    "/wallets/{wallet_id}",
    status_code=200,
    response_model=WalletItemEnvelope,
)
def show_wallet(
        wallet_id: UUID,
        users: UserRepositoryDependable,
        API_key: UUID = Header(alias="API_key")
) -> dict[str, dict] | JSONResponse:
    try:
        wallet = users.get_wallet(API_key, wallet_id)
        response_data = extract_wallet_fields(wallet)
        return {"wallet": response_data}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Wallet does not exist."},
        )


@wallet_api.get(
    "/wallets/{address}/transactions",
    status_code=200,
    response_model=TransactionListEnvelope,
)
def show_transaction(
        address: UUID,
        users: UserRepositoryDependable,
        API_key: UUID = Header(alias="API_key")
) -> dict[str, dict] | JSONResponse:
    try:
        transactions = users.get_wallet(API_key, address).transactions
        return {"transactions": transactions}
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Wallet does not exist."},
        )
