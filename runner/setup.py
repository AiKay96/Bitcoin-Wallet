import os

from fastapi import FastAPI

from infra.in_database.user_sqlite import UserInDatabase
from infra.in_database.wallet_sqlite import WalletInDatabase
from infra.in_memory.statistics import StatisticInMemory
from infra.in_memory.transactions import TransactionInMemory
from infra.in_memory.users import UserInMemory
from infra.wallet_api.statistics_api import statistic_api
from infra.wallet_api.transactions_api import transaction_api
from infra.wallet_api.users_api import user_api
from infra.in_memory.wallets import WalletInMemory
from infra.wallet_api.wallets_api import wallet_api


def init_app():
    app = FastAPI()
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)
    app.include_router(statistic_api)

    os.environ["REPOSITORY_KIND"] = "sqlite"

    # need to change if/else.
    if os.getenv("REPOSITORY_KIND", "memory") == "sqlite":
        app.state.wallets = WalletInDatabase()
        app.state.users = UserInDatabase()
    else:
        app.state.users = UserInMemory()
        app.state.wallets = WalletInMemory()
        app.state.transactions = TransactionInMemory()
        app.state.statistics = StatisticInMemory()

    return app
