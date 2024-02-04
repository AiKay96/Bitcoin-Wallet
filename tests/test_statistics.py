import uuid
from dataclasses import dataclass, field
from typing import Any

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from core.constants import ADMIN_API_KEY, COMMISSION
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


def make_user(client: TestClient) -> uuid:
    user = Fake().user()
    response = client.post("/users", json=user)
    return response.json()["user"]["API_key"]


def make_wallet(client: TestClient, API_key: uuid) -> uuid:
    response = client.post("/wallets", json={"API_key": API_key})
    return response.json()["wallet"]["address"]


def test_not_show_statistics(client: TestClient) -> None:
    API_key = Fake().unknown_id()
    response = client.get("/statistics", headers={"API_key": API_key})

    assert response.status_code == 403
    assert response.json() == {'message': 'User does not have access to statistics.'}


def test_show_statistics_different_user(client: TestClient) -> None:
    user1 = make_user(client)
    wallet1 = make_wallet(client, user1)
    user2 = make_user(client)
    wallet2 = make_wallet(client, user2)

    client.post("/transactions",
                json={"API_key": user1, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100})

    response = client.get("/statistics", headers={"API_key": ADMIN_API_KEY})

    assert response.status_code == 200
    assert response.json()["statistics"]["profit_in_satoshis"] == round(100 * COMMISSION)


def test_show_statistics_multiple_transactions(client: TestClient) -> None:
    user1 = make_user(client)
    wallet1 = make_wallet(client, user1)
    user2 = make_user(client)
    wallet2 = make_wallet(client, user2)

    for i in range(3):
        client.post("/transactions",
                    json={"API_key": user1, "wallet_from": wallet1, "wallet_to": wallet2,
                          "amount_in_satoshis": 100})

    response = client.get("/statistics", headers={"API_key": ADMIN_API_KEY})

    assert response.status_code == 200
    assert response.json()["statistics"]["transaction_number"] == 3


def test_show_statistics_different_transactions(client: TestClient) -> None:
    user1 = make_user(client)
    wallet1 = make_wallet(client, user1)
    user2 = make_user(client)
    wallet2 = make_wallet(client, user2)
    wallet3 = make_wallet(client, user2)

    client.post("/transactions",
                json={"API_key": user1, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100})

    client.post("/transactions",
                json={"API_key": user2, "wallet_from": wallet2, "wallet_to": wallet3,
                      "amount_in_satoshis": 200})

    response = client.get("/statistics", headers={"API_key": ADMIN_API_KEY})

    assert response.status_code == 200
    assert response.json()["statistics"]["profit_in_satoshis"] == round(100 * COMMISSION)


def test_show_statistics_same_user(client: TestClient) -> None:
    user = make_user(client)
    wallet1 = make_wallet(client, user)
    wallet2 = make_wallet(client, user)

    client.post("/transactions",
                json={"API_key": user, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100})

    response = client.get("/statistics", headers={"API_key": ADMIN_API_KEY})

    assert response.status_code == 200
    assert response.json()["statistics"]["profit_in_satoshis"] == 0
