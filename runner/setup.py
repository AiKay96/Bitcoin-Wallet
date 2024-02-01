import os

from fastapi import FastAPI

from infra.in_memory.users import UserInMemory
from infra.wallet_api.users_api import user_api


def init_app():
    app = FastAPI()
    app.include_router(user_api)

    # need to change if/else.
    if os.getenv("BOOK_REPOSITORY_KIND", "memory") == "sqlite":
        ...
    else:
        app.state.users = UserInMemory()

    return app
