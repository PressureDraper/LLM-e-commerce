from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.infrastructure.database.session import get_db
from app.modules.auth.jwt import get_current_user
from app.modules.auth.schemas import AddressCreate, AddressResponse, TokenPayload, TokenResponse, UserLogin, UserRegister, UserResponse, UserUpdate
from app.modules.auth.service import AuthService


router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:  # Object injection helper
    return AuthService(db)


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: UserRegister, service: AuthService = Depends(get_service)):
    return await service.register(body)


@router.post("/login", response_model=UserResponse)
async def login(body: UserLogin, response: Response, service: AuthService = Depends(get_service)):
    user, token = await service.login(body)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="strict",
        max_age=settings.JWT_EXPIRE_MINUTES * 60
    )

    return user


@router.post("/logout", status_code=204)
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="strict"
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(request: Request, service: AuthService = Depends(get_service)):
    current_user = get_current_user(request)
    return await service.get_profile(current_user.sub)


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    body: UserUpdate,
    request: Request,
    service: AuthService = Depends(get_service)
):
    current_user = get_current_user(request)
    return await service.update_profile(current_user.sub, body)


@router.get("/profile/addresses", response_model=list[UserResponse])
async def get_addresses(
    request: Request,
    service: AuthService = Depends(get_service)
):
    current_user = get_current_user(request)
    return await service.get_addresses(current_user.sub)


@router.post("/profile/addresses", response_model=AddressResponse, status_code=201)
async def create_address(
    body: AddressCreate,
    request: Request,
    service: AuthService = Depends(get_service)
):
    current_user = get_current_user(request)
    return await service.create_address(current_user.sub, body)
