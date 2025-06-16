from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from models.base import Base
from sqlalchemy.sql import func


class ScrapedProduct(Base):
    __tablename__ = "scraped_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("scrape_requests.id"))
    marketplace_id: Mapped[int] = mapped_column(ForeignKey("marketplaces.id"))
    scraped_product_title: Mapped[str] = mapped_column(String)
    scraped_price: Mapped[str] = mapped_column(String, nullable=True)
    scraped_currency: Mapped[str] = mapped_column(String, nullable=True)
    product_url: Mapped[str] = mapped_column(String, nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            "marketplace_id",
            "product_url",
            name="uix_scraped_products_request_marketplace_url",
        ),
    )
