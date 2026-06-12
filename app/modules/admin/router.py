from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.modules.admin.schemas import SettingsResponse
from app.modules.admin.services import AdminService


router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(db)


@router.get("/settings", response_model=SettingsResponse)
async def get_settings(service: AdminService = Depends(get_service)):
    return await { "sail": True, "data": service.get_settings() }
