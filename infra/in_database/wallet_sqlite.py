from dataclasses import dataclass


@dataclass
class WalletInDatabase:
    db_path: str = "./database.db"
