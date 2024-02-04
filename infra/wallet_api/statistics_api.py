from uuid import UUID

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import AccessError

from infra.wallet_api.dependables import StatisticRepositoryDependable

statistic_api = APIRouter(tags=["Statistics"])


class StatisticItem(BaseModel):
    transaction_number: int
    profit_in_satoshis: float


class StatisticItemEnvelope(BaseModel):
    statistic: StatisticItem


@statistic_api.get(
    "/statistics",
    status_code=200,
    response_model=StatisticItemEnvelope,
)
def show_statistic(
        statistics: StatisticRepositoryDependable,
        API_key: UUID = Header(alias="API_key")
) -> dict[str, dict] | JSONResponse:
    try:
        statistics = statistics.get(API_key)
        return {"statistics": statistics}
    except AccessError:
        return JSONResponse(
            status_code=403,
            content={"message": f"User does not have access to statistics."},
        )
