from typing import List, Optional

from domain.order import Order
from domain.order_book import OrderBook
from domain.order_response import OrderResponse

from domain.order_book_response import OrderBookResponse
from domain.order_side import OrderSide
from infrastructure.order_model import OrderModel


class OrderMapper:
    @staticmethod
    def to_domain(row: OrderModel) -> Order:
        print(row.side)
        return Order(
            order_id=row.id,
            symbol=row.symbol,
            price=row.price,
            quantity=row.quantity,
            side=OrderSide(row.side),
            decimals=row.decimals,
            is_open=row.is_open,
        )

    @staticmethod
    def to_domain_order_book(rows: List[OrderModel]) -> OrderBook:
        if not rows:
            return OrderBook({})
        return OrderBook({row.id: OrderMapper.to_domain(row) for row in rows})

    @staticmethod
    def to_order_book_response(book: OrderBook) -> OrderBookResponse:
        return OrderBookResponse(
            orders={order_id: OrderMapper.to_order_response(order) for order_id, order in book.orders.items()}
        )

    @staticmethod
    def to_model(entity: Order, order_model: Optional[OrderModel] = None) -> OrderModel:
        if order_model:
            order_model.symbol = entity.symbol
            order_model.side = entity.side.value
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

    @staticmethod
    def to_order_response(order: Order) -> OrderResponse:
        return OrderResponse(
            order_id=order.order_id,
            symbol=order.symbol,
            price=order.price,
            quantity=order.quantity,
            side=order.side,
            decimals=order.decimals,
            is_open=order.is_open,
        )
