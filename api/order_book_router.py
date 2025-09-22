from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.dependencies import get_order_service
from api.metadata import Metadata
from api.order_request import OrderRequest
from api.success_response import SuccessResponse, SuccessResponseModel
from application.order_service import OrderService
from domain.order_response import OrderResponse

from domain.order_book_response import OrderBookResponse
from domain.order_mapper import OrderMapper
from domain.order_side import OrderSide

order_book_router = APIRouter()


@order_book_router.get("/health")
def health_check():
    """
    Health check endpoint for container health monitoring.
    """
    return {"status": "healthy", "service": "order-matching"}


@order_book_router.get("/open",
                       response_model=SuccessResponseModel[OrderBookResponse],
                       description="Retrieve all open orders from the order book, with optional filtering by "
                                   "symbol, side, and price.",
                       summary="Retrieve all open orders from the order book"
                       )
def get_open_orders(
        symbol: Optional[str] = Query(None),
        side: Optional[OrderSide] = Query(None),
        price: Optional[int] = Query(None),
        order_service: OrderService = Depends(get_order_service)
) -> SuccessResponse:
    """
    Retrieve all open orders from the order book.
    """
    start_time = datetime.now(timezone.utc)
    order_book = order_service.fetch_open_orders(symbol, side, price)
    return SuccessResponse(
        metadata=Metadata.from_start_time(start_time),
        response_data=OrderMapper.to_order_book_response(order_book)
    )


@order_book_router.post("/add",
                        response_model=SuccessResponseModel[OrderResponse],
                        description="Add a new order to the order book, fill if possible and return the order details.",
                        summary="Add a new order to the order book"
                        )
def add_order(order_request: OrderRequest
              , order_service: OrderService = Depends(get_order_service)
              ) -> SuccessResponse:
    """
    Add a new order to the order book.
    """
    start_time = datetime.now(timezone.utc)
    order = order_service.add_order(order_request)
    return SuccessResponse(
        metadata=Metadata.from_start_time(start_time),
        response_data=OrderMapper.to_order_response(order)
    )
