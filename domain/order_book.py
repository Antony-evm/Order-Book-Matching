from typing import Dict

from .order import Order


class OrderBook:
    def __init__(
            self,
            orders: Dict[int, Order]
    ):
        self.orders = orders if orders else {}

    def add_order(self, order: Order):
        self.orders[order.order_id] = order

    def remove_order(self, order: Order):
        self.orders.pop(order.order_id, None)

    def to_dict(self) -> dict:
        return {"orders": {order_id: order.to_dict() for order_id, order in self.orders.items()}}

