import uuid
from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import Integer, String, Text, DateTime, Uuid, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.core.database import Base

class Item(Base):
    __tablename__ = 'items'

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_item_price_non_negative"),
        CheckConstraint("count >= 0", name="check_item_count_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(),primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    mini_description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
