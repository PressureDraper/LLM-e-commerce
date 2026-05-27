from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.modules.auth.jwt import get_current_user
from app.modules.auth.schemas import TokenPayload, TokenResponse, UserLogin, UserRegister, UserResponse
from app.modules.auth.service import AuthService


router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:  # Object injection helper
    return AuthService(db)


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: UserRegister, service: AuthService = Depends(get_service)):
    return await service.register(body)


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin, service: AuthService = Depends(get_service)):
    return await service.login(body)


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: TokenPayload = Depends(get_current_user), service: AuthService = Depends(get_service)):
    return await service.get_profile(current_user.sub)
