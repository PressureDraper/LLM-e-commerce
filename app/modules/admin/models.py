from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, IDMixin, TimestampMixin


class Settings(Base, IDMixin, TimestampMixin):
    __tablename__ = "site_settings"

    site_name: Mapped[str] = mapped_column(String(100), nullable=False)
    site_logo_url: Mapped[str] = mapped_column(String(255), nullable=False)
    favicon_url: Mapped[str | None] = mapped_column(String(255))

    login_img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    
    hero_img_url: Mapped[str | None] = mapped_column(String(255))
    hero_video_url: Mapped[str | None] = mapped_column(String(255))
