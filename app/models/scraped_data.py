from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class ScrapedProductData(Base):
    __tablename__ = "scraped_product_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    url_on_platform = Column(String)
    name_on_platform = Column(String)
    price = Column(Float)
    currency = Column(String)
    rating = Column(Float)
    reviews_count = Column(Integer)
    availability_status = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    search_position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="scraped_data")
    platform = relationship("Platform", back_populates="scraped_data")
