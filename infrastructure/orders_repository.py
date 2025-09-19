from typing import Type

from sqlalchemy.orm import Session

from domain.order import Order
from domain.order_mapper import OrderMapper
from .order_model import OrderModel


class OrdersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_open_order_by_id(self, order_id: int) -> OrderModel | None:
        """Fetch a single OrderBook entry by ID"""
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()

    def create_order(self, order: OrderModel) -> OrderModel:
        """Add a new OrderBook entry"""
        self.db.add(order)
        self.db.flush()
        self.db.refresh(order)
        return order

    def update_order(self, order: Order) -> OrderModel:
        order_model = self.get_open_order_by_id(order.order_id)
        if not order_model:
            raise ValueError(f"Order with ID {order.order_id} not found")
        order_model = OrderMapper.to_model(order, order_model)
        self.db.flush()
        self.db.refresh(order_model)
        return order_model

    def get_open_orders(
            self,
            symbol: str = None,
            side: str = None,
            price: int = None
    ) -> list[Type[OrderModel]]:
        """Fetch all open OrderBook entries"""
        result = self.db.query(OrderModel).filter(OrderModel.is_open == True)
        if symbol:
            result = result.filter(OrderModel.symbol == symbol)
        if side:
            result = result.filter(OrderModel.side == side)
        if price:
            result = result.filter(OrderModel.price == price)
        return result.order_by(OrderModel.id).all()

