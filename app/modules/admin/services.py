from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.admin.repository import AdminRepository
from app.modules.admin.schemas import SettingsResponse


class AdminService:
    def __init__(self, db: AsyncSession):
        self.repo = AdminRepository(db)

    async def get_settings(self) -> SettingsResponse:
        settings = await self.repo.get_settings()

        return SettingsResponse.model_validate(settings)