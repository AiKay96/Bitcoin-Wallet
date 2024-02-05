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
            connection.commit()

    def clear_tables(self) -> None:
        update_statistics_query = '''
               UPDATE statistics SET transaction_number = 0, profit_in_satoshis = 0;
           '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(update_statistics_query)
            connection.commit()

    def get(self, key: UUID) -> Statistic:
        if key != UUID(ADMIN_API_KEY):
            raise AccessError("Statistics not available.")

        get_statistic_query = '''
               SELECT transaction_number, profit_in_satoshis FROM statistics;
           '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(get_statistic_query)
            statistic_data = cursor.fetchone()

            return Statistic(
                transaction_number=statistic_data[0],
                profit_in_satoshis=statistic_data[1]
            )

    def update(self, commission: int) -> None:
        select_statistic_query = '''SELECT * FROM statistics'''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(select_statistic_query)
            statistic_data = cursor.fetchone()
            if statistic_data is None:
                insert_default_statistic_query = '''
                    INSERT INTO statistics (transaction_number, profit_in_satoshis) VALUES (0, 0);
                '''
                cursor.execute(insert_default_statistic_query)
                connection.commit()

        update_statistic_query = '''
            UPDATE statistics SET transaction_number = transaction_number + 1, profit_in_satoshis = profit_in_satoshis + ?;
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(update_statistic_query, (commission,))
            connection.commit()
