from typing import Dict

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from openerp.config import Config


class Database:
    client: AsyncIOMotorClient = AsyncIOMotorClient(Config.MONGO_URI)
    db: AsyncIOMotorDatabase = client['OpenErps']

    @classmethod
    async def connect(cls):
        """Connect to the MongoDB database."""
        cls.client = AsyncIOMotorClient(Config.MONGO_URI)
        cls.db: AsyncIOMotorDatabase = cls.client['OpenErps']
        logger.debug("Connected to MongoDB")

    @classmethod
    async def disconnect(cls):
        """Disconnect from the MongoDB database."""
        if cls.client:
            cls.client.close()
            logger.debug("Disconnected from MongoDB")

    @classmethod
    def get_collection(cls, collection_name: str) -> AsyncIOMotorCollection:
        """Get a collection from the database."""
        return cls.db[collection_name]

    @classmethod
    async def create_db_indexes(cls, collection_name: str, indexes: Dict[str, int]):
        """
        Create indexes on a collection.
        """
        collection = cls.get_collection(collection_name)
        index_tuples = [(key, direction) for key, direction in indexes.items()]
        await collection.create_indexes([{'key': index_tuples}])
        logger.debug(f"Indexes created on collection {collection_name}: {indexes}")
