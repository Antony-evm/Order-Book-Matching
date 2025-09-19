"""create orders table

Revision ID: e096b9644ab8
Revises: 
Create Date: 2025-09-18 05:43:10.299032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e096b9644ab8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("symbol", sa.String(), nullable=True, index=False),  # index added below
        sa.Column("side", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("decimals", sa.Integer(), nullable=False, server_default=sa.text("2")),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("is_open", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    # index to match `index=True` on symbol
    op.create_index(op.f("ix_orders_symbol"), "orders", ["symbol"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_orders_symbol"), table_name="orders")
    op.drop_table("orders")
