import sqlite3
from dataclasses import dataclass
from uuid import UUID

from core.constants import ADMIN_API_KEY
from core.errors import AccessError
from core.statistics import Statistic


@dataclass
class StatisticInDatabase:
    def __init__(self, db_path: str = "./database.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS statistics (
                transaction_number INTEGER NOT NULL,
                profit_in_satoshis INTEGER NOT NULL
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)

    def clear_tables(self) -> None:
        truncate_units_query = """
            DELETE FROM statistics;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(truncate_units_query)
            connection.commit()

    def get(self, key: UUID) -> Statistic:
        get_statistic_query = '''
            SELECT * FROM statistics;
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(get_statistic_query)
            statistic_data = cursor.fetchone()

            if key == ADMIN_API_KEY:
                return Statistic(
                    transaction_number=statistic_data[0],
                    profit_in_satoshis=statistic_data[1]
                )
            else:
                raise AccessError("Statistics not available.")

    def update(self, commission: int) -> None:
        update_statistic_query = '''
            UPDATE statistics SET transaction_number = transaction_number + 1, profit_in_satoshis = profit_in_satoshis + ?;
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(update_statistic_query, (commission,))
            connection.commit()
