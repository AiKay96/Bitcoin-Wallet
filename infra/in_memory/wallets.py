from dataclasses import dataclass
from core.wallets import Wallet


@dataclass
class WalletInMemory:
    def create(self, wallet: Wallet) -> Wallet:
        pass

