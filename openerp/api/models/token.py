from datetime import UTC, datetime

from openerp.api.models.base import Base


class Token(Base):
    id: str
    user_id: str
    active: bool = True
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime | None = None
    ttl: datetime | None = None


class JwtPayload(Base):
    sub: str
    exp: datetime
    tid: str
