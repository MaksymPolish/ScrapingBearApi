from pydantic import BaseModel
from typing import List, Union, Optional
from datetime import datetime


class ScrapingConfig(BaseModel):
    product_name: str
    marketplace_ids: Optional[List[int]] = None


class ScrapingResultSuccess(BaseModel):
    marketplace_name: str
    status: str
    product_title: str
    price: str
    url: str
    scraped_at: datetime


class ScrapingResultError(BaseModel):
    marketplace_name: str
    status: str
    error_message: str
    scraped_at: datetime


ScrapingResult = Union[ScrapingResultSuccess, ScrapingResultError]


class Summary(BaseModel):
    total_marketplaces_processed: int
    successful_scrapes: int
    failed_scrapes: int


class ScrapingResults(BaseModel):
    scrape_request_id: int
    product_name_searched: str
    results: List[ScrapingResult]
    summary: Summary


class ScrapedProductCreate(BaseModel):
    request_id: int
    marketplace_id: int
    scraped_product_title: str
    scraped_price: Optional[str] = None
    scraped_currency: Optional[str] = None
    product_url: Optional[str] = None
    status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ScrapedProductResponse(BaseModel):
    id: int
    request_id: int
    marketplace_id: int
    scraped_product_title: str
    scraped_price: Optional[str] = None
    scraped_currency: Optional[str] = None
    product_url: Optional[str] = None
    scraped_at: datetime
    status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ScrapeRequestResponse(BaseModel):
    id: int
    product_name_searched: str
    requested_at: datetime

    class Config:
        from_attributes = True
