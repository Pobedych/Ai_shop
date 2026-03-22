from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from datetime import datetime, timezone

from app.backend.core.database import Base

import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tg_id = Column(BigInteger, primary_key=True, nullable=False)

    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(String, nullable=False, default='USER')

    balance = Column(BigInteger, nullable=False, default=0)
    purchase_count = Column(BigInteger, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
