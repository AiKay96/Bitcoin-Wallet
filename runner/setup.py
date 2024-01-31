import os

from fastapi import FastAPI


def init_app():
    app = FastAPI()
    # app.include_router(...)

    # need to change if/else.
    # if os.getenv("BOOK_REPOSITORY_KIND", "memory") == "sqlite":
    #     ...
    # else:
    #     ...

    return app
