from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.auth.models import User, UserAddress


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id, User.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str, full_name: str | None, role: str = "customer") -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        self.db.add(user)
        await self.db.flush()
        return user
    
    async def create_oauth_user(self, email: str, full_name: str | None, avatar_url: str, provider: str) -> User:
        user = User(
            email=email,
            hashed_password=None,
            full_name=full_name,
            avatar_url=avatar_url,
            oauth_provider=provider,
            role="customer",
            is_verified=True
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def update(self, user: User, data: dict) -> User:
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        await self.db.flush()
        return user

    async def get_addresses(self, user_id: int) -> list[UserAddress]:
        result = await self.db.execute(
            select(UserAddress).where(
                UserAddress.user_id == user_id,
                UserAddress.deleted_at.is_(None),
            )
        )
        return list(result.scalars().all())

    async def create_address(self, user_id: int, data: dict) -> UserAddress:
        if data.get("is_default"):
            await self._clear_default_address(user_id)

        address = UserAddress(user_id=user_id, **data)
        self.db.add(address)
        await self.db.flush()
        return address

    async def _clear_default_address(self, user_id: int) -> None:
        result = await self.db.execute(
            select(UserAddress).where(
                UserAddress.user_id == user_id,
                UserAddress.is_default.is_(True),
            )
        )
        for address in result.scalars().all():
            address.is_default = False
