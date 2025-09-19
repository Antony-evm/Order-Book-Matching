from pydantic import BaseModel, Field

from domain.order_side import OrderSide


class OrderRequest(BaseModel):
    symbol: str = Field(..., description="The trading symbol, e.g., 'AAPL'")
    quantity: int = Field(..., gt=0, description="The quantity of the order, must be greater than 0")
    side: OrderSide = Field(..., description="The side of the order, either 'buy' or 'sell'")
    price: int = Field(..., gt=0, description="The price of the order, must be greater than 0")
    decimals: int = Field(2, ge=0, le=8, description="Number of decimal places for the price")
