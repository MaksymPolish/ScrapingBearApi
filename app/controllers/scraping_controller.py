from fastapi import APIRouter, Query
from typing import Annotated
from services.scraping_service import ScrapingServiceDependency
from schemas.scraping import (
    ScrapingConfig,
    ScrapingResults,
    ScrapedProductResponse,
    ScrapeRequestResponse,
)
from crud.scraping_repository import ScrapingRepositoryDependency

scraping_router = APIRouter(prefix="/scraping", tags=["scraping"])


@scraping_router.post("/scrape-product", response_model=ScrapingResults)
async def scrape_product(
    service: ScrapingServiceDependency,
    config: ScrapingConfig,
):
    return await service.scrape_product(config)


@scraping_router.get("/scraped-products", response_model=list[ScrapedProductResponse])
async def get_scraped_products(
    repo: ScrapingRepositoryDependency,
    id: Annotated[int | None, Query()] = None,
    request_id: Annotated[int | None, Query()] = None,
    marketplace_id: Annotated[int | None, Query()] = None,
):
    return await repo.fetch_scraped_products(id, request_id, marketplace_id)


@scraping_router.get("/scrape-requests", response_model=list[ScrapeRequestResponse])
async def get_all_scrape_requests(
    repo: ScrapingRepositoryDependency,
):
    return await repo.list_scrape_requests()


@scraping_router.get(
    "/scrape-request/{request_id}", response_model=ScrapeRequestResponse
)
async def get_scrape_request(
    request_id: int,
    repo: ScrapingRepositoryDependency,
):
    return await repo.fetch_scrape_request(request_id)
