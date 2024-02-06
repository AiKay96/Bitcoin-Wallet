import os

from fastapi import FastAPI

from BitcoinWallet.infra.in_database.statistic_sqlite import StatisticInDatabase
from BitcoinWallet.infra.in_database.transaction_sqlite import TransactionInDatabase
from BitcoinWallet.infra.in_database.user_sqlite import UserInDatabase
from BitcoinWallet.infra.in_database.wallet_sqlite import WalletInDatabase
from BitcoinWallet.infra.in_memory.statistics import StatisticInMemory
from BitcoinWallet.infra.in_memory.transactions import TransactionInMemory
from BitcoinWallet.infra.in_memory.users import UserInMemory
from BitcoinWallet.infra.in_memory.wallets import WalletInMemory
from BitcoinWallet.infra.wallet_api.statistics_api import statistic_api
from BitcoinWallet.infra.wallet_api.transactions_api import transaction_api
from BitcoinWallet.infra.wallet_api.users_api import user_api
from BitcoinWallet.infra.wallet_api.wallets_api import wallet_api


def init_app() -> FastAPI:
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
        app.state.statistics = StatisticInDatabase()
        app.state.transactions = TransactionInDatabase()
    else:
        app.state.users = UserInMemory()
        app.state.wallets = WalletInMemory()
        app.state.transactions = TransactionInMemory()
        app.state.statistics = StatisticInMemory()

    return app
