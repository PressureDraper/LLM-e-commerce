from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

# ── DTOs ──────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, word: str) -> str:
        if len(word) < 8:
            raise ValueError("Password must be at least 8 characters")
        return word


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    role: str
    exp: datetime


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    role: str
    is_active: bool
    is_verified: bool
    avatar_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None


class AddressCreate(BaseModel):
    alias: str
    full_name: str
    phone: str
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "México"
    notes: str | None = None
    is_default: bool = False


class AddressResponse(AddressCreate):
    id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}