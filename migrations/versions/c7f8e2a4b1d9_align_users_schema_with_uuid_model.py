"""align users schema with uuid model

Revision ID: c7f8e2a4b1d9
Revises: bc380ff60f42
Create Date: 2026-04-01 19:05:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c7f8e2a4b1d9"
down_revision: Union[str, Sequence[str], None] = "bc380ff60f42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Сначала подготовим таблицу для миграции данных
    users_table = sa.table(
        "users",
        sa.column("is_active", sa.Boolean()),
        sa.column("balance", sa.Numeric()),
    )

    # 2. Безопасно заполняем возможные NULL перед изменением на NOT NULL
    # (на случай, если данные были добавлены в обход ограничений или они были изменены)
    op.execute(
        users_table.update()
        .where(users_table.c.is_active.is_(None))
        .values(is_active=True)
    )
    op.execute(
        users_table.update()
        .where(users_table.c.balance.is_(None))
        .values(balance=sa.text("0.00"))
    )

    # 3. Изменяем колонки
    # Переход со String на Uuid в Postgres требует явного приведения типов
    op.alter_column(
        "users",
        "id",
        existing_type=sa.String(),
        type_=sa.Uuid(),
        postgresql_using="id::uuid",
        existing_nullable=False,
    )

    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("true"),
    )

    op.alter_column(
        "users",
        "balance",
        existing_type=sa.BigInteger(),
        type_=sa.Numeric(10, 2),
        postgresql_using="balance::numeric(10,2)",
        existing_nullable=False,
        server_default=sa.text("0.00"),
    )

def downgrade() -> None:
    op.alter_column(
        "users",
        "balance",
        existing_type=sa.Numeric(10, 2),
        type_=sa.BigInteger(),
        postgresql_using="balance::bigint",
        existing_nullable=False,
        server_default=None,
    )
    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=None,
    )
    op.alter_column(
        "users",
        "id",
        existing_type=sa.Uuid(),
        type_=sa.String(),
        postgresql_using="id::text",
        existing_nullable=False,
    )
