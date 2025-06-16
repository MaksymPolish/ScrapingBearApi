from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped
from models.base import Base


class Marketplace(Base):
    __tablename__ = "marketplaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    base_search_url: Mapped[str] = mapped_column(String)
    product_selector: Mapped[str] = mapped_column(String)
    title_selector: Mapped[str] = mapped_column(String)
    price_selector: Mapped[str] = mapped_column(String)
    link_selector: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
