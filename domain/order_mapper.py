from typing import Sequence, Type, List, Optional
from infrastructure.order_model import OrderModel
from domain.order import Order
from domain.order_book import OrderBook


class OrderMapper:
    @staticmethod
    def to_domain(row: OrderModel) -> Order:
        return Order(
            order_id=row.id,
            symbol=row.symbol,
            price=row.price,
            quantity=row.quantity,
            side=row.side,
            decimals=row.decimals,
            is_open=row.is_open,
        )

    @staticmethod
    def to_domain_order_book(rows: List[Type[OrderModel]]) -> OrderBook:
        if not rows:
            return OrderBook({})
        return OrderBook({row.id: OrderMapper.to_domain(row) for row in rows})

    @staticmethod
    def to_model(entity: Order, order_model: Optional[OrderModel] = None) -> OrderModel:
        if order_model:
            order_model.symbol = entity.symbol
            order_model.side = entity.side
            order_model.price = entity.get_price()
            order_model.decimals = entity.decimals
            order_model.quantity = entity.get_quantity()
            order_model.is_open = entity.is_open
            return order_model

        return OrderModel(
            id=entity.get_order_id(),
            symbol=entity.symbol,
            side=entity.side.value,
            price=entity.get_price(),
            decimals=entity.decimals,
            quantity=entity.get_quantity(),
            is_open=entity.is_open,
        )
