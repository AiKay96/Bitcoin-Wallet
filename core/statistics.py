from dataclasses import dataclass
from uuid import UUID
from typing import Protocol

from core.constants import ADMIN_API_KEY


@dataclass
class Statistic:
    transaction_number: int = 0
    profit_in_satoshis: int = 0


class StatisticRepository(Protocol):
    def get(self, key: UUID) -> Statistic:
        pass

    def update(self, commission: float) -> None:
        pass


@dataclass
class StatisticsService:
    statistics: StatisticRepository
