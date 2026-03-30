"""create items table

Revision ID: 3d4b0d6a9f21
Revises: aa0b537312b2
Create Date: 2026-03-25 16:35:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3d4b0d6a9f21"
down_revision: Union[str, Sequence[str], None] = "aa0b537312b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("mini_description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("price >= 0", name="check_item_price_non_negative"),
        sa.CheckConstraint("count >= 0", name="check_item_count_non_negative"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_items")),
        sa.UniqueConstraint("name", name=op.f("uq_items_name")),
    )
    op.create_index(op.f("ix_items_category"), "items", ["category"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_items_category"), table_name="items")
    op.drop_table("items")
