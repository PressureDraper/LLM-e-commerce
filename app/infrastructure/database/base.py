import re
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Shared base fro all SQLAlchemy models.
    Generates __tablename__ from classname.

    Ej: class ProductCategory -> tabla: product_categories
    """

    @classmethod
    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if "__tablename__" not in cls.__dict__:
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
            cls.__tablename__ = f"{name}s"


class IDMixin:
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)


class TimestampMixin:
    """
    class Product(Base, IDMixin, TimestampMixin):
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )
