import os

import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from application.order_service import OrderService
from infrastructure.database import Base
from infrastructure.order_model import OrderModel
from infrastructure.orders_repository import OrdersRepository


@pytest.fixture(scope="session")
def engine():
    url = os.getenv("TEST_DATABASE_URL")
    eng = create_engine(url, future=True, echo=True, poolclass=NullPool)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    trans = connection.begin()

    SessionLocal = sessionmaker(bind=connection, autoflush=False, expire_on_commit=False, future=True)
    session = SessionLocal()
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def _restart_savepoint(sess, txn):
        if txn.nested and not connection.closed:
            connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        nested.rollback()
        trans.rollback()
        connection.close()


@pytest.fixture
def orders_repository(db_session):
    return OrdersRepository(db_session)

@pytest.fixture
def order_service(orders_repository):
    return OrderService(orders_repository)
