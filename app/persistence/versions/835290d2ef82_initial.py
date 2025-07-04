"""initial

Revision ID: 835290d2ef82
Revises:
Create Date: 2025-06-06 15:16:27.677568

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "835290d2ef82"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "marketplaces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("base_search_url", sa.String(), nullable=False),
        sa.Column("product_selector", sa.String(), nullable=False),
        sa.Column("title_selector", sa.String(), nullable=False),
        sa.Column("price_selector", sa.String(), nullable=False),
        sa.Column("link_selector", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "scrape_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_name_searched", sa.String(), nullable=False),
        sa.Column(
            "requested_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "scraped_products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.Integer(), nullable=False),
        sa.Column("marketplace_id", sa.Integer(), nullable=False),
        sa.Column("scraped_product_title", sa.String(), nullable=False),
        sa.Column("scraped_price", sa.String(), nullable=True),
        sa.Column("scraped_currency", sa.String(), nullable=True),
        sa.Column("product_url", sa.String(), nullable=True),
        sa.Column(
            "scraped_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["marketplace_id"],
            ["marketplaces.id"],
        ),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["scrape_requests.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "request_id",
            "marketplace_id",
            "product_url",
            name="uix_scraped_products_request_marketplace_url",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("scraped_products")
    op.drop_table("scrape_requests")
    op.drop_table("marketplaces")
    # ### end Alembic commands ###
