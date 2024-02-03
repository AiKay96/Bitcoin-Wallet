from dataclasses import dataclass, field
from typing import Any
from unittest.mock import ANY

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from runner.setup import init_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def user(self) -> dict[str, Any]:
        return {
            "username": self.faker.word(),
            "password": self.faker.word()
        }


def test_should_create(client: TestClient) -> None:
    user = Fake().user()

    response = client.post("/users", json=user)

    assert response.status_code == 201
    assert response.json() == {"user": {"API_key": ANY, **user}}


def test_should_not_create_same(client: TestClient) -> None:
    user = Fake().user()

    response = client.post("/users", json=user)

    assert response.status_code == 201
    assert response.json() == {"user": {"API_key": ANY, **user}}

    response = client.post("/users", json=user)

    assert response.status_code == 409
    assert response.json() == {'message': 'User already exists.'}
