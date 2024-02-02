from dataclasses import dataclass, field
from uuid import UUID

from core.errors import ExistsError
from core.users import User


@dataclass
class UserInMemory:
    users: dict[UUID, User] = field(default_factory=dict)

    def create(self, user: User) -> User:
        for existing_user in self.users.values():
            if existing_user.username == user.username:
                raise ExistsError("User already exists.")

        self.users[user.API_key] = user
        return user
