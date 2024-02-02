import os

from fastapi import FastAPI

from infra.in_memory.users import UserInMemory
from infra.wallet_api.users_api import user_api
from infra.in_memory.wallets import WalletInMemory
from infra.wallet_api.wallets_api import wallet_api


def init_app():
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(wallet_api)

    # need to change if/else.
    if os.getenv("BOOK_REPOSITORY_KIND", "memory") == "sqlite":
        ...
    else:
        app.state.users = UserInMemory()
        app.state.wallets = WalletInMemory()

    return app
