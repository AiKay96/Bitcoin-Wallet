import sqlite3
from uuid import UUID

from core import constants
from core.errors import CapacityError, DoesNotExistError
from core.users import User
from core.wallets import Wallet


class WalletInDatabase:
    def __init__(self, db_path: str = "./database.db") -> None:
        self.db_path = db_path
        self.create_table()

    def create_table(self) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS wallets (
                API_KEY TEXT PRIMARY KEY,
                balance INT,
                address TEXT
            );
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_query)

    def clear_tables(self) -> None:
        truncate_units_query = """
            DELETE FROM wallets;
        """
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(truncate_units_query)
            connection.commit()

    # useristvis chasamatebelia +1 wallet.
    def create(self, wallet: Wallet, user: User) -> Wallet:
        if user.wallets_number == constants.MAXIMUM_NUMBER_OF_WALLETS:
            raise CapacityError

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO wallets (API_key, balance, address)
                VALUES (?, ?, ?)
                """,
                (wallet.API_key, wallet.balance, wallet.address)
            )
            connection.commit()

        return wallet

    def get(self, key: UUID) -> Wallet:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT API_key, balance, address
                FROM wallets
                WHERE address = ?
                """,
                (str(key),)
            )
            result = cursor.fetchone()

        if result is None:
            raise DoesNotExistError(f"Wallet with key {key} does not exist.")

        wallet = Wallet(API_key=result[0], balance=result[1], address=result[2])

        return wallet

    def get_user_wallets(self, API_key: UUID) -> list[Wallet]:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT API_key, balance, address
                FROM wallets
                WHERE API_key = ?
                """,
                (str(API_key),)
            )
            results = cursor.fetchall()

        wallets = []
        for result in results:
            wallet = Wallet(API_key=result[0], balance=result[1], address=result[2])
            wallets.append(wallet)

        return wallets
