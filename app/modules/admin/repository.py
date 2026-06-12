from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.admin.models import Settings


class AdminRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_settings(self) -> Settings:
        result = await self.db.execute(
            select(Settings)
            .order_by(Settings.created_at.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()
