from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import ExistsError
from core.transactions import Transaction
from infra.wallet_api.dependables import TransactionRepositoryDependable

transaction_api = APIRouter(tags=["Transactions"])


