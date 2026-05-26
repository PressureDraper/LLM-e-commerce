from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.jwt import create_access_token
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import TokenResponse, UserLogin, UserRegister, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)
    
    async def register(self, data: UserRegister) -> UserResponse:
        existing = await self.repo.get_by_email(data.email)

        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        
        hashed_password = pwd_context.hash(data.password)
        user = await self.repo.create(data.email, hashed_password, data.full_name)

        return UserResponse.model_validate(user)
    
    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No user found with these credentials")
        
        if not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
        
        token = create_access_token(user.id, user.role)
        return TokenResponse(access_token=token)
        


