from datetime import UTC, datetime, timedelta

import jwt
import pydantic

from openerp.api.models.token import JwtPayload
from openerp.api.operations.token import TokenOps
from openerp.config import Config
from openerp.exceptions.token import InvalidTokenException


class TokenUtil:
    secret_key = Config.SECRET_KEY
    token_ops = TokenOps()

    async def _create_access_token(self, payload: JwtPayload) -> str:
        """Create a JWT access token."""
        expire = datetime.now(UTC) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.exp = expire
        return jwt.encode(payload.model_dump(), self.secret_key, algorithm="HS256")

    async def create_token(self, user_id: str) -> tuple[str, str]:
        """Create a JWT token"""
        expire = datetime.now(UTC) + timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
        token_id = await self.token_ops.add_token(user_id)
        payload = JwtPayload(sub=user_id, exp=expire, tid=token_id)
        refresh_token = jwt.encode(payload.model_dump(), self.secret_key, algorithm="HS256")
        access_token = await self._create_access_token(payload)

        return access_token, refresh_token

    async def verify_token(self, token: str) -> JwtPayload:
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return JwtPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("Trying to decode expired JWT token")
        except jwt.InvalidTokenError:
            raise InvalidTokenException("Trying to decode invalid JWT token")
        except pydantic.ValidationError:
            raise InvalidTokenException("Trying to serealize valid JWT token with invalid payload")

    async def revoke_token(self, token_id: str) -> None:
        """Invalidate a token"""
        await self.token_ops.revoke_token(token_id)

    async def refresh_access_token(self, refresh_token: str) -> str:
        """Refresh the access token using a refresh token"""
        payload = await self.verify_token(refresh_token)

        valid = await self.token_ops.refresh_token(payload.tid)
        if not valid:
            raise InvalidTokenException("User is trying to refresh an revoked token")

        new_access_token = await self._create_access_token(payload)
        return new_access_token
