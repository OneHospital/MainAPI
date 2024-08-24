from datetime import UTC, datetime, timedelta

from bson import ObjectId

from openerp.api.models.token import Token
from openerp.config import Config
from openerp.database import Database


class TokenOps:
    def __init__(self):
        self.collection = Database.get_collection("tokens")

    async def add_token(self, user_id: str) -> str:
        """Insert a new token into the collection."""
        ttl_days = Config.REFRESH_TOKEN_EXPIRE_DAYS
        token_info = {
            "active": True,
            "user_id": ObjectId(user_id),
            "created_at": datetime.now(UTC),
            "updated_at": None,
            "ttl": datetime.now(UTC) + timedelta(days=ttl_days)
        }
        inserted = await self.collection.insert_one(token_info)
        return str(inserted.inserted_id)

    async def revoke_token(self, token_id: str) -> None:
        """Invalidate a token"""
        await self.collection.update_one(
            {"_id": ObjectId(token_id)},
            {"$set": {"active": False, "ttl": datetime.now(UTC)}}
        )

    async def get_all_sessions(self, user_id: str, active_only: bool = True) -> list[Token]:
        """Get all tokens for a user"""
        if active_only:
            tokens = self.collection.find({"user_id": ObjectId(user_id), "active": True})
        else:
            tokens = self.collection.find({"user_id": ObjectId(user_id)})

        final_tokens = []

        async for token in tokens:
            token_obj = Token(**token, id=token["_id"])
            final_tokens.append(token_obj)

        return final_tokens

    async def refresh_token(self, token_id: str) -> bool:
        """Validate a refresh token"""
        token = await self.collection.find_one({"_id": ObjectId(token_id), "active": True})
        if token:
            await self.collection.update_one(
                {"_id": ObjectId(token_id)},
                {"$set": {"updated_at": datetime.now(UTC)}}
            )
        return bool(token)
