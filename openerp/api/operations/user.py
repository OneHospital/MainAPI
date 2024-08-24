from loguru import logger

from openerp.database import Database


class UserOps:
    def __init__(self):
        self.collection = Database.get_collection("users")

    async def find_user_by_email(self, email: str) -> dict | None:
        """Find a user by email."""
        return await self.collection.find_one({"email": email})

    async def create_user(self, user_info: dict) -> str:
        """Insert a new user into the collection."""
        inserted = await self.collection.insert_one(user_info)
        if inserted.acknowledged:
            logger.debug(f"User created with email: {user_info['email']}")
        return str(inserted.inserted_id)

    async def update_user(self, email: str, updates: dict) -> str:
        """Update an existing user's information."""
        user = await self.find_user_by_email(email)
        inserted = await self.collection.update_one({"email": email}, {"$set": updates})
        if inserted.acknowledged:
            logger.debug(f"User updated with email: {email}")
        return str(user.get("_id"))
