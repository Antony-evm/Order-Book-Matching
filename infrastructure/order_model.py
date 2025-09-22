from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from .database import Base


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    decimals = Column(Integer, default=2, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
