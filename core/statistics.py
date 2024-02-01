from dataclasses import dataclass
from uuid import UUID
from typing import Protocol


@dataclass
class Statistics:
    ADMIN_key: UUID
    transaction_number: int
    profit: float


class StatisticsRepository(Protocol):
    pass


@dataclass
class StatisticsService:
    statistics: StatisticsRepository
