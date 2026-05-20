from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base, IDMixin, TimestampMixin
from app.modules.auth.models import User
from app.modules.products.models import Product


class Order(Base, IDMixin, TimestampMixin):
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
        # pending / confirmed / shipped / delivered / cancelled
    )

    # ── Pricing ───────────────────────────────────────────────────────────────
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_cost: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # ── Payment ───────────────────────────────────────────────────────────────
    payment_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="unpaid"
        # unpaid / paid / refunded
    )
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(
        String(255), nullable=True
        # transaction ID
    )

    # ── Shipping snapshot ─────────────────────────────────────────────────────
    # saving shipping details as a snapshot in the order, so we keep the history despite user_adress changes
    shipping_full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    shipping_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    shipping_street: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_city: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_state: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    shipping_country: Mapped[str] = mapped_column(String(100), nullable=False)
    shipping_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── FK ────────────────────────────────────────────────────────────────────
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # ── Relations ─────────────────────────────────────────────────────────────
    user: Mapped["User | None"] = relationship(
        "User", back_populates="orders"
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base, IDMixin, TimestampMixin):
    __tablename__ = "order_items"

    # ── Product snapshot ──────────────────────────────────────────────────────
    # storing product details at buying time for preserving snapshot even if product data changes later
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    product_slug: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # ── FK ─────────────────────────────────────────────────────────────────────
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True
    )

    # ── Relations ─────────────────────────────────────────────────────────────
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product | None"] = relationship("Product")