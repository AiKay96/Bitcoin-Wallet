from dataclasses import dataclass, field
from uuid import UUID

from core.errors import CapacityError
from core.users import User
from core.wallets import Wallet


@dataclass
class WalletInMemory:
    wallets: dict[UUID, Wallet] = field(default_factory=dict)

    def create(self, wallet: Wallet, user: User) -> Wallet:
        if user.wallets_number == 3:
            raise CapacityError
        self.wallets[wallet.address] = wallet
        return wallet

