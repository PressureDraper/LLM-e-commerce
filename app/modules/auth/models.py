from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, IDMixin, TimestampMixin
from app.modules.orders.models import Order


class User(Base, IDMixin, TimestampMixin):
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    role: Mapped[str] = mapped_column(String(20), nullable=False, default="customer")    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="user"
    )
    addresses: Mapped[list["UserAddress"]] = relationship(
        "UserAddress", back_populates="user", cascade="all, delete-orphan"
    )


class UserAddress(Base, IDMixin, TimestampMixin):
    __tablename__ = "user_addresses"

    alias: Mapped[str] = mapped_column(String(50), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="México")
    notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── FK ────────────────────────────────────────────────────────────────────
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # ── Relations ─────────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="addresses")