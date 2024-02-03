from dataclasses import dataclass, field
from uuid import UUID

from core import constants
from core.errors import CapacityError, DoesNotExistError
from core.users import User
from core.wallets import Wallet


@dataclass
class WalletInMemory:
    wallets: dict[UUID, Wallet] = field(default_factory=dict)

    def create(self, wallet: Wallet, user: User) -> Wallet:
        if user.wallets_number == constants.MAXIMUM_NUMBER_OF_WALLETS:
            raise CapacityError
        self.wallets[wallet.address] = wallet
        user.wallets[wallet.address] = wallet
        user.wallets_number += 1
        return wallet

    def get(self, key: UUID) -> Wallet:
        wallet = self.wallets.get(key)
        if wallet is None:
            raise DoesNotExistError(f"User with key {key} does not exist.")
        return wallet
