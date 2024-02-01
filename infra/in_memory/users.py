from dataclasses import dataclass, field
from uuid import UUID

from core.users import User


@dataclass
class UserInMemory:
    users: dict[UUID, User] = field(default_factory=dict)

    def create(self, user: User) -> User:
        self.users[user.API_key] = user
        return user
