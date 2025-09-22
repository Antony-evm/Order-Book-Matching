from typing import Dict

from pydantic import BaseModel

from domain.order_response import OrderResponse


class OrderBookResponse(BaseModel):
    orders: Dict[int, OrderResponse]