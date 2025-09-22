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

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return (
                self.order_id == other.order_id and
                self.symbol == other.symbol and
                self.price == other.price and
                self.quantity == other.quantity and
                self.side == other.side and
                self.decimals == other.decimals and
                self.is_open == other.is_open
        )

    def __repr__(self):
        return (f"Order(id={self.order_id}, symbol={self.symbol}, side={self.side}, price={self.price},"
                f" quantity={self.quantity}, is_open={self.is_open})")

