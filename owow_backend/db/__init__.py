from beanie import init_beanie
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from owow_backend.core import logger
from owow_backend.db.models import load_all_models
from owow_backend.settings import settings


class MongoConnection:
    def __init__(self) -> None:
        self.url: str = settings.mongo_host
        self.client: AgnosticClient[AsyncIOMotorDatabase] = AsyncIOMotorClient(  # type: ignore
            self.url,
        )

    async def connect(self) -> None:
        logger.info("Connecting to MongoDB....")
        await init_beanie(
            database=self.client["OWOW"],  # type: ignore
            document_models=load_all_models(),  # type: ignore
        )
        logger.info("Connected to MongoDB")
