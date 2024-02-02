from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from core.users import UserRepository
from core.wallets import WalletRepository


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.users  # type: ignore


UserRepositoryDependable = Annotated[
    UserRepository, Depends(get_user_repository)
]


def get_wallet_repository(request: Request) -> WalletRepository:
    return request.app.state.wallets  # type: ignore


WalletRepositoryDependable = Annotated[
    WalletRepository, Depends(get_wallet_repository)
]
