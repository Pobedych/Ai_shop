import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    String,
    Uuid,
    Numeric,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column


from app.backend.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[int] = mapped_column(
        BigInteger(), unique=True, index=True, nullable=False
    )

    username: Mapped[str] = mapped_column(String(), nullable=True)
    first_name: Mapped[str] = mapped_column(String(), nullable=True)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    email: Mapped[str] = mapped_column(String(), nullable=True)
    phone: Mapped[str] = mapped_column(String(), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    role: Mapped[str] = mapped_column(String(), nullable=False, default="USER")
    language: Mapped[str] = mapped_column(String(), nullable=False, default="en")

    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    purchase_count: Mapped[int] = mapped_column(BigInteger(), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )
