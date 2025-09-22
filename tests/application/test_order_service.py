import pytest
from sqlalchemy import text

from api.order_request import OrderRequest
from domain.order import Order
from domain.order_side import OrderSide
from infrastructure.order_model import OrderModel


@pytest.fixture
def seed_orders(db_session):
    """
    Truncate and seed deterministic orders for each test, then return a dict of IDs.
    """
    db_session.execute(text("TRUNCATE TABLE orders RESTART IDENTITY CASCADE"))

    rows = [
        OrderModel(symbol="AAPL", side="buy", price=100, decimals=2, quantity=5, is_open=True),
        OrderModel(symbol="AAPL", side="buy", price=100, decimals=2, quantity=3, is_open=True),
        OrderModel(symbol="AAPL", side="buy", price=101, decimals=2, quantity=1, is_open=True),
        OrderModel(symbol="AAPL", side="sell", price=100, decimals=2, quantity=2, is_open=True),
        OrderModel(symbol="AAPL", side="sell", price=100, decimals=2, quantity=2, is_open=False),
        OrderModel(symbol="TSLA", side="buy", price=100, decimals=2, quantity=4, is_open=True),
        OrderModel(symbol="TSLA", side="sell", price=101, decimals=2, quantity=6, is_open=True),
    ]
    db_session.add_all(rows)
    db_session.flush()


@pytest.mark.parametrize(
    "symbol,side,price,expected_count",
    [
        (None, None, None, 6),
        ("AAPL", None, None, 4),
        ("TSLA", None, None, 2),
        (None, OrderSide.BUY, None, 4),
        (None, OrderSide.SELL, None, 2),
        ("AAPL", OrderSide.BUY, None, 3),
        (None, None, 100, 4),
        ("AAPL", OrderSide.BUY, 100, 2),
        ("SP500", None, None, 0),
    ]
)
def test_fetch_open_orders_no_filters(order_service, seed_orders, symbol, side, price, expected_count):
    order_book = order_service.fetch_open_orders(symbol=symbol, side=side, price=price)
    assert len(order_book.orders) == expected_count


@pytest.mark.parametrize(
    "order_request, expected", [
        (
                OrderRequest(symbol="SP500", side=OrderSide.BUY, price=100, quantity=10, decimals=2),
                Order(symbol="SP500", side=OrderSide.BUY, price=100, quantity=10, order_id=8)
        ),
        (
                OrderRequest(symbol="AAPL", side=OrderSide.BUY, price=110, quantity=10, decimals=2),
                Order(symbol="AAPL", side=OrderSide.BUY, price=110, quantity=10, order_id=8)
        ),
        (
                OrderRequest(symbol="AAPL", side=OrderSide.BUY, price=100, quantity=10, decimals=2),
                Order(symbol="AAPL", side=OrderSide.BUY, price=100, quantity=8, order_id=8)
        ),
        (
                OrderRequest(symbol="AAPL", side=OrderSide.BUY, price=100, quantity=1, decimals=2),
                Order(symbol="AAPL", side=OrderSide.BUY, price=100, quantity=0, order_id=8, is_open=False)
        )
    ]
)
def test_adding_order(order_service, seed_orders, order_request, expected):
    order = order_service.add_order(order_request)
    assert order == expected
