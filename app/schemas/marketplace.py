from pydantic import BaseModel
from datetime import datetime


class MarketplaceCreateUpdate(BaseModel):
    name: str
    base_search_url: str
    product_selector: str
    title_selector: str
    price_selector: str
    link_selector: str


class MarketplaceResponse(MarketplaceCreateUpdate):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
