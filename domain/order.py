from domain.order_side import OrderSide


class Order:
    def __init__(
            self,
            symbol: str,
            price: int,
            quantity: int,
            side: OrderSide,
            decimals: int = 2,
            is_open: bool = True,
            order_id: int = None
    ):
        self.order_id = order_id
        self.symbol = symbol
        self.price = price
        self.decimals = decimals
        self.quantity = quantity
        self.side = side
        self.is_open = is_open

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def set_is_open(self, is_open: bool):
        self.is_open = is_open

    def get_quantity(self) -> int:
        return self.quantity

    def get_price(self) -> int:
        return self.price

    def get_order_id(self) -> int:
        return self.order_id

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "price": self.price,
            "quantity": self.quantity,
            "side": self.side,
            "decimals": self.decimals,
            "is_open": self.is_open,
        }
