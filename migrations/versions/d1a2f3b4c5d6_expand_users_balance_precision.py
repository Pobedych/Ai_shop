"""expand users balance precision

Revision ID: d1a2f3b4c5d6
Revises: c7f8e2a4b1d9
Create Date: 2026-04-04 18:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1a2f3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "c7f8e2a4b1d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "balance",
        existing_type=sa.Numeric(10, 2),
        type_=sa.Numeric(18, 2),
        existing_nullable=False,
        existing_server_default=sa.text("0.00"),
        server_default=sa.text("0.00"),
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "balance",
        existing_type=sa.Numeric(18, 2),
        type_=sa.Numeric(10, 2),
        existing_nullable=False,
        existing_server_default=sa.text("0.00"),
        server_default=sa.text("0.00"),
    )
