import sqlite3
from dataclasses import dataclass

from core.errors import ExistsError
from core.users import User


@dataclass
class UserInDatabase:
    db_path: str = "./database.db"

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                API_key TEXT NOT NULL,
                wallets_number INTEGER NOT NULL
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)

    def clear_tables(self) -> None:
        truncate_units_query = """
            DELETE FROM users;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(truncate_units_query)
            connection.commit()

    def create(self, user: User) -> User:
        self.create_table()

        create_user_query = '''
            INSERT INTO users (API_KEY, username, password, wallets_number)
            VALUES (?, ?, ?, ?)
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM users WHERE username = ?', (user.username,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise ExistsError("User already exists.")

            cursor.execute(create_user_query, (str(user.API_key), user.username, user.password, user.wallets_number))
            connection.commit()

        return user



