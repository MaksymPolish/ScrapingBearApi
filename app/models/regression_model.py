from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime

class RegressionModel(Base):
    __tablename__ = "regression_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    target_variable = Column(String)
    feature_variables = Column(JSON)
    coefficients_json = Column(JSON)
    intercept = Column(Float)
    last_trained_at = Column(DateTime)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    platform = relationship("Platform", back_populates="regression_models")
