from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import DoesNotExistError, CapacityError
from core.wallets import Wallet
from infra.wallet_api.dependables import WalletRepositoryDependable

wallet_api = APIRouter(tags=["Wallets"])


def extract_wallet_fields(wallet: Wallet) -> dict:
    return {
        "address": wallet.address,
        "balance_in_BTC": wallet.balance,
        "balance_in_USD": wallet.balance_in_usd()
    }


class CreateWalletRequest(BaseModel):
    API_key: UUID


class WalletItem(BaseModel):
    address: UUID
    balance_in_BTC: float
    balance_in_USD: float


class WalletItemEnvelope(BaseModel):
    wallet: WalletItem


@wallet_api.post(
    "/wallets",
    status_code=201,
    response_model=WalletItemEnvelope,
)
def create_wallet(
        request: CreateWalletRequest, wallets: WalletRepositoryDependable
) -> dict[str, dict] | JSONResponse:
    try:
        wallet = Wallet(**request.model_dump())
        wallets.create(wallet)

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
