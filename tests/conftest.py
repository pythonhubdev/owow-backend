from typing import Any, AsyncGenerator

import pytest
from beanie import init_beanie
from fastapi import FastAPI
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from owow_backend.db.models import FileDocument, UserDocument, load_all_models
from owow_backend.settings import Settings
from owow_backend.settings import settings as app_settings
from owow_backend.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Fixture to create database connection.

    :yield: nothing.
    """
    client = AsyncIOMotorClient(app_settings.mongo_host)  # type: ignore

    await init_beanie(
        database=client["TestDatabase"],
        document_models=load_all_models(),  # type: ignore
    )
    yield


@pytest.fixture
def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    return application


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :param anyio_backend: backend for anyio pytest plugin.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test/api", timeout=2.0) as ac:
        yield ac


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(mongo_host="mongodb://localhost:27017", environment="TEST", predibase_token="test_token")


@pytest.fixture(scope="session")
async def init_db(settings: Settings) -> AsyncGenerator[None, None]:
    client = AsyncIOMotorClient(settings.mongo_host)  # type: ignore
    await init_beanie(database=client.test_db, document_models=[UserDocument, FileDocument])
    yield
    await client.drop_database("test_db")


@pytest.fixture(scope="function")
async def clean_db(init_db: None) -> AsyncGenerator[None, None]:
    yield
    await UserDocument.delete_all()
    await FileDocument.delete_all()
