from pydantic import BaseModel

from domain.order_side import OrderSide


class OrderResponse(BaseModel):
    order_id: int | None
    symbol: str
    price: int
    quantity: int
    side: OrderSide
    decimals: int = 2
    is_open: bool = True
