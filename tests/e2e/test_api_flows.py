import asyncio
from uuid import UUID

import be_task_ca.app as app_module
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from be_task_ca.app import app
from be_task_ca.database import Base


def _prepare_test_db(monkeypatch) -> None:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(app_module, "SessionLocal", testing_session_local)


async def _post(path: str, payload: dict) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.post(path, json=payload)


async def _get(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(path)


def test_e2e_create_user_flow(monkeypatch):
    _prepare_test_db(monkeypatch)

    response = asyncio.run(
        _post(
            "/users/",
            {
                "first_name": "Marko",
                "last_name": "Crnic",
                "email": "marko@example.com",
                "password": "password",
                "shipping_address": "Street 1",
            },
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "marko@example.com"
    assert UUID(body["id"])


def test_e2e_create_item_flow(monkeypatch):
    _prepare_test_db(monkeypatch)

    response = asyncio.run(
        _post(
            "/items/",
            {
                "name": "Keyboard",
                "description": "Mechanical",
                "price": 99.0,
                "quantity": 5,
            },
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Keyboard"
    assert UUID(body["id"])


def test_e2e_add_item_to_cart_flow(monkeypatch):
    _prepare_test_db(monkeypatch)

    created_user = asyncio.run(
        _post(
            "/users/",
            {
                "first_name": "Marko",
                "last_name": "Crnic",
                "email": "marko@example.com",
                "password": "password",
                "shipping_address": "Street 1",
            },
        )
    ).json()
    created_item = asyncio.run(
        _post(
            "/items/",
            {
                "name": "Keyboard",
                "description": "Mechanical",
                "price": 99.0,
                "quantity": 5,
            },
        )
    ).json()

    response = asyncio.run(
        _post(
            f"/users/{created_user['id']}/cart",
            {"item_id": created_item["id"], "quantity": 2},
        )
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["item_id"] == created_item["id"]
    assert body["items"][0]["quantity"] == 2


def test_e2e_get_items_flow(monkeypatch):
    _prepare_test_db(monkeypatch)

    asyncio.run(
        _post(
            "/items/",
            {
                "name": "Book",
                "description": "Clean Architecture",
                "price": 19.99,
                "quantity": 3,
            },
        )
    )

    response = asyncio.run(_get("/items/"))

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Book"
