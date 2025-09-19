from enum import Enum


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def reversed(self):
        return OrderSide.SELL if self == OrderSide.BUY else OrderSide.BUY
