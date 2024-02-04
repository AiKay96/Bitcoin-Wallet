import uuid
from dataclasses import dataclass, field
from typing import Any
from unittest.mock import ANY

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from core import constants
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

    def unknown_id(self) -> uuid:
        return self.faker.uuid4()


def test_should_create(client: TestClient) -> None:
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]

    response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 201
    assert response.json()["wallet"]["balance_in_BTC"] == 1


def test_should_not_create(client: TestClient) -> None:
    API_key = Fake().unknown_id()

    response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 404
    assert response.json() == {'message': 'User does not exists.'}


def test_should_not_4_wallet(client: TestClient) -> None:
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]
    for i in range(constants.MAXIMUM_NUMBER_OF_WALLETS + 1):
        response = client.post("/wallets", json={"API_key": API_key})
    assert response.status_code == 403
    assert response.json() == {'message': 'User has reached the maximum capacity of wallets.'}


def test_should_not_read_without_user(client: TestClient) -> None:
    API_key = Fake().unknown_id()
    address = Fake().unknown_id()
    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 404
    assert response.json() == {"message": f"Wallet does not exist."}


def test_should_not_read_without_address(client: TestClient) -> None:
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]
    address = Fake().unknown_id()
    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 404
    assert response.json() == {"message": f"Wallet does not exist."}


def test_should_persist(client: TestClient) -> None:
    user = Fake().user()
    response = client.post("/users", json=user)
    API_key = response.json()["user"]["API_key"]

    response = client.post("/wallets", json={"API_key": API_key})
    address = response.json()["wallet"]["address"]

    response = client.get(f"/wallets/{address}", headers={"API_key": API_key})

    assert response.status_code == 200
    assert response.json()["wallet"]["balance_in_BTC"] == 1
