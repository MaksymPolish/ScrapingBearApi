from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from models.base import Base
from sqlalchemy.sql import func


class ScrapeRequest(Base):
    __tablename__ = "scrape_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name_searched: Mapped[str] = mapped_column(String)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
