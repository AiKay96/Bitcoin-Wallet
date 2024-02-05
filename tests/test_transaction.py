import os
import uuid
from dataclasses import dataclass, field
from typing import Any

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from core import constants
from infra.in_database.transaction_sqlite import TransactionInDatabase
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


def clear_tables() -> None:
    if os.getenv("REPOSITORY_KIND", "memory") == "sqlite":
        TransactionInDatabase().clear_table()


def test_should_create_transaction_same_user(client: TestClient) -> None:
    clear_tables()
    API_key = make_user(client)
    wallet_from = make_wallet(client, API_key)
    wallet_to = make_wallet(client, API_key)
    response = client.post("/transactions",
                           json={"API_key": API_key, "wallet_from": wallet_from, "wallet_to": wallet_to,
                                 "amount_in_satoshis": 100})
    assert response.status_code == 201
    assert response.json() == {}


def test_should_create_transaction(client: TestClient) -> None:
    clear_tables()
    API_key1 = make_user(client)
    wallet_from = make_wallet(client, API_key1)
    API_key2 = make_user(client)
    wallet_to = make_wallet(client, API_key2)
    response = client.post("/transactions",
                           json={"API_key": API_key1, "wallet_from": wallet_from, "wallet_to": wallet_to,
                                 "amount_in_satoshis": 100})
    assert response.status_code == 201
    assert response.json() == {}


def test_should_not_create(client: TestClient) -> None:
    clear_tables()
    API_key = Fake().unknown_id()
    wallet_from = Fake().unknown_id()
    wallet_to = Fake().unknown_id()

    response = client.post("/transactions",
                           json={"API_key": API_key, "wallet_from": wallet_from, "wallet_to": wallet_to,
                                 "amount_in_satoshis": 100})
    assert response.status_code == 404
    assert response.json() == {'message': 'Wallet does not exist.'}


def test_equal_error(client: TestClient) -> None:
    clear_tables()
    API_key = make_user(client)
    wallet = make_wallet(client, API_key)

    response = client.post("/transactions",
                           json={"API_key": API_key, "wallet_from": wallet, "wallet_to": wallet,
                                 "amount_in_satoshis": 100})
    assert response.status_code == 400
    assert response.json() == {'message': 'Transaction within the same wallet is not allowed.'}


def test_balance_error(client: TestClient) -> None:
    clear_tables()
    API_key1 = make_user(client)
    wallet1 = make_wallet(client, API_key1)
    API_key2 = make_user(client)
    wallet2 = make_wallet(client, API_key2)

    client.post("/transactions",
                json={"API_key": API_key1, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100000000})
    response = client.post("/transactions",
                           json={"API_key": API_key1, "wallet_from": wallet1, "wallet_to": wallet2,
                                 "amount_in_satoshis": 100000000})

    assert response.status_code == 400
    assert response.json() == {'message': 'Not enough balance to complete the transaction.'}


def test_transaction_validity(client: TestClient) -> None:
    clear_tables()
    API_key1 = make_user(client)
    wallet1 = make_wallet(client, API_key1)
    API_key2 = make_user(client)
    wallet2 = make_wallet(client, API_key2)

    response = client.get(f"/wallets/{wallet1}", headers={"API_key": API_key1})
    balance_before1 = response.json()["wallet"]["balance_in_BTC"]

    client.post("/transactions",
                json={"API_key": API_key1, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100})

    response = client.get(f"/wallets/{wallet1}", headers={"API_key": API_key1})
    balance_after1 = response.json()["wallet"]["balance_in_BTC"]

    assert round((balance_before1 - balance_after1) * constants.BTC_TO_SATOSHI, 8) == 100


def test_get_transactions(client: TestClient) -> None:
    clear_tables()
    API_key1 = make_user(client)
    API_key2 = make_user(client)
    wallet1 = make_wallet(client, API_key1)
    wallet2 = make_wallet(client, API_key2)

    client.post("/transactions",
                json={"API_key": API_key1, "wallet_from": wallet1, "wallet_to": wallet2,
                      "amount_in_satoshis": 100})

    client.post("/transactions",
                json={"API_key": API_key2, "wallet_from": wallet2, "wallet_to": wallet1,
                      "amount_in_satoshis": 100})

    response = client.get("/transactions", headers={"API_key": API_key1})

    assert response.status_code == 200
    assert len(response.json()["transactions"]) == 2

    response = client.get("/transactions", headers={"API_key": API_key2})
    assert response.status_code == 200
    assert len(response.json()["transactions"]) == 2


def test_get_transactions_empty(client: TestClient) -> None:
    clear_tables()
    API_key = make_user(client)
    response = client.get("/transactions", headers={"API_key": API_key})

    assert response.status_code == 200
    assert len(response.json()["transactions"]) == 0


def test_should_not_get_transactions(client: TestClient) -> None:
    clear_tables()
    API_key = Fake().unknown_id()
    response = client.get("/transactions", headers={"API_key": API_key})

    assert response.status_code == 404
    assert response.json() == {'message': 'User does not exist.'}
