from api.order_request import OrderRequest
from domain.order import Order
from domain.order_book import OrderBook
from domain.order_mapper import OrderMapper
from domain.order_side import OrderSide
from infrastructure.orders_repository import OrdersRepository


class OrderService:

    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    def fetch_open_orders(
            self,
            symbol: str = None,
            side: OrderSide = None,
            price: int = None
    ) -> OrderBook:
        if side:
            side = side.value
        orders = self.orders_repository.get_open_orders(symbol, side, price)
        return OrderMapper.to_domain_order_book(orders)

    def add_order(self, order_request: OrderRequest) -> Order:
        order = Order(
            symbol=order_request.symbol,
            quantity=order_request.quantity,
            side=order_request.side,
            price=order_request.price,
            decimals=order_request.decimals
        )
        order_book = self.fetch_open_orders(
            symbol=order_request.symbol, side=order_request.side.reversed(), price=order_request.price
        )
        order_model = self.orders_repository.create_order(OrderMapper.to_model(order))
        order = OrderMapper.to_domain(order_model)
        if order_book.orders:
            self._match_orders(order, order_book)
        order = OrderMapper.to_domain(order_model)
        return order

    def _match_orders(self, order: Order, order_book: OrderBook):
        for order_id in order_book.orders.keys():
            existing_order = order_book.orders.get(order_id)
            quantity_to_fill = existing_order.get_quantity()
            quantity = order.get_quantity()
            if quantity > quantity_to_fill:
                self._update_order(order, quantity - quantity_to_fill)
                self._update_order(existing_order, 0)
            elif quantity == quantity_to_fill:
                self._update_order(order, 0)
                self._update_order(existing_order, 0)
                break
            else:
                self._update_order(existing_order, quantity_to_fill - quantity)
                self._update_order(order, 0)
                break

    def _update_order(self, order: Order, quantity: int):
        order.set_quantity(quantity)
        if quantity == 0:
            order.set_is_open(is_open=False)
        self.orders_repository.update_order(order)
