import sqlite3
from dataclasses import dataclass
from uuid import UUID

from core.errors import ExistsError, DoesNotExistError
from core.transactions import Transaction
from core.users import User
from core.wallets import Wallet


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
            connection.commit()

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

    def get(self, key: UUID) -> User:
        get_user_query = '''
            SELECT * FROM users WHERE API_key = ?
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(get_user_query, (str(key),))
            user_data = cursor.fetchone()

            if user_data:
                return User(username=user_data[0], password=user_data[1], API_key=UUID(user_data[2]),
                            wallets_number=user_data[3])
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def increment_wallets_number(self, key: UUID) -> int:
        increment_query = '''
            UPDATE users SET wallets_number = wallets_number + 1 WHERE API_key = ?
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(increment_query, (str(key),))
            connection.commit()

            cursor.execute('SELECT wallets_number FROM users WHERE API_key = ?', (str(key),))
            updated_wallets_number = cursor.fetchone()

            if updated_wallets_number:
                return updated_wallets_number[0]
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def get_wallet(self, key: UUID, address: UUID) -> Wallet:
        user_query = '''
            SELECT * FROM users WHERE API_key = ?
        '''

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()

            cursor.execute(user_query, (str(key),))
            user_data = cursor.fetchone()

            if user_data:
                wallet_query = '''
                    SELECT * FROM wallets WHERE API_key = ? AND address = ?
                '''
                cursor.execute(wallet_query, (str(key), str(address)))
                wallet_data = cursor.fetchone()

                if wallet_data:
                    return Wallet(address=UUID(wallet_data[0]), balance=wallet_data[1], API_key=key)
                else:
                    raise DoesNotExistError("User does not have this wallet")
            else:
                raise DoesNotExistError(f"User with key {key} does not exist.")

    def get_transactions(self, key: UUID) -> list[Transaction]:
        self.get(key)
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT API_key, balance, address
                FROM wallets
                WHERE API_key = ?
                """,
                (str(key),)
            )
            results = cursor.fetchall()

        wallets = []
        for result in results:
            wallet = Wallet(API_key=result[0], balance=result[1], address=result[2])
            wallets.append(wallet)
        answer: list[Transaction] = []

        addresses = [""] * 3

        for i, wallet in enumerate(wallets[:3]):
            addresses[i] = wallet.address

        user_query = '''
                    SELECT * FROM wallet_transactions WHERE wallet_from = ? or wallet_from = ? or wallet_from = ? 
                                    or wallet_to = ? or wallet_to = ? or wallet_to = ?
                '''
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(user_query, (
                str(addresses[0]), str(addresses[1]), str(addresses[2]), str(addresses[0]), str(addresses[1]),
                str(addresses[2]),))
            data = cursor.fetchall()

            for result in data:
                transaction = Transaction(
                    wallet_from=result[0],
                    wallet_to=result[1],
                    amount_in_satoshis=result[2]
                )
                answer.append(transaction)

        return answer
