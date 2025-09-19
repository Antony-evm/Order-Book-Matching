from fastapi import Depends
from sqlalchemy.orm import Session

from application.order_service import OrderService
from infrastructure.database import get_db
from infrastructure.orders_repository import OrdersRepository


def get_orders_repository(
        db: Session = Depends(get_db)
) -> OrdersRepository:
    return OrdersRepository(db)


def get_order_service(
        orders_repository: OrdersRepository = Depends(get_orders_repository)
) -> OrderService:
    return OrderService(orders_repository)

