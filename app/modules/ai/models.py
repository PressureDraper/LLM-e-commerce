

from langchain import messages
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, IDMixin, TimestampMixin
from app.modules.auth.models import User


class ChatSession(Base, IDMixin, TimestampMixin):
    __tablename__ = "chat_sessions"

    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    #auto generated from first message

    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    user: Mapped["User | None"] = relationship("User")
    messages: Mapped[list["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base, IDMixin, TimestampMixin):
    __tablename__ = "chat_messages"

    role: Mapped[str] = mapped_column(String(20), nullable=False) # user / assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # ── RAG METADATA ────────────────────────────────────────────────────────────────────
    retrieved_product_ids: Mapped[str | None] = mapped_column(Text, nullable=True)  # "1,5,23" — Product IDs pgvector retrieves

    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)

    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")