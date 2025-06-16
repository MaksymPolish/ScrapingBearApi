from fastapi import Depends, HTTPException
from db import SessionContext
from models.scrape_request import ScrapeRequest
from models.scraped_product import ScrapedProduct
from typing import Annotated, List
from sqlalchemy import select, insert
from schemas.scraping import ScrapedProductCreate


class ScrapingRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def add_scrape_request(self, product_name: str) -> ScrapeRequest:
        scrape_req = ScrapeRequest(product_name_searched=product_name)
        self.session.add(scrape_req)
        await self.session.commit()
        return scrape_req

    async def add_scraped_product(
        self, product_info: ScrapedProductCreate
    ) -> ScrapedProduct:
        stmt = (
            insert(ScrapedProduct)
            .values(**product_info.model_dump())
            .returning(ScrapedProduct)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def fetch_scraped_products(
        self,
        product_id: int | None = None,
        req_id: int | None = None,
        market_id: int | None = None,
    ) -> List[ScrapedProduct]:
        stmt = select(ScrapedProduct)
        if product_id is not None:
            stmt = stmt.where(ScrapedProduct.id == product_id)
        else:
            if req_id is not None:
                stmt = stmt.where(ScrapedProduct.request_id == req_id)
            if market_id is not None:
                stmt = stmt.where(ScrapedProduct.marketplace_id == market_id)
        result = await self.session.execute(stmt)
        products = result.scalars().all()
        if product_id is not None and not products:
            raise HTTPException(status_code=404, detail="Scraped product not found")
        return list(products)

    async def list_scrape_requests(self) -> List[ScrapeRequest]:
        res = await self.session.execute(select(ScrapeRequest))
        return list(res.scalars().all())

    async def fetch_scrape_request(self, req_id: int) -> ScrapeRequest:
        res = await self.session.execute(
            select(ScrapeRequest).where(ScrapeRequest.id == req_id)
        )
        req = res.scalar_one_or_none()
        if req is None:
            raise HTTPException(status_code=404, detail="Scrape request not found")
        return req


ScrapingRepositoryDependency = Annotated[
    ScrapingRepository, Depends(ScrapingRepository)
]
