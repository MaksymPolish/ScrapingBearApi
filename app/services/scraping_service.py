from typing import List, Annotated
from fastapi import HTTPException, Depends
from datetime import datetime, timezone
import re
from schemas.scraping import (
    ScrapingConfig,
    ScrapingResultSuccess,
    ScrapingResultError,
    ScrapingResults,
    Summary,
    ScrapedProductCreate,
)
from crud.scraping_repository import ScrapingRepositoryDependency
from crud.marketplace_repository import MarketplaceRepositoryDependency
from services.scraping_utils import scrape_product_data


class ScrapingService:
    def __init__(
        self,
        repo_marketplace: MarketplaceRepositoryDependency,
        repo_scraping: ScrapingRepositoryDependency,
    ):
        self.repo_marketplace = repo_marketplace
        self.repo_scraping = repo_scraping

    async def scrape_product(self, config: ScrapingConfig) -> ScrapingResults:
        # Отримати всі активні маркетплейси
        active_marketplaces = await self.repo_marketplace.get_all_active_marketplaces()

        # Визначити, які маркетплейси використовувати
        if config.marketplace_ids:
            id_set = set(config.marketplace_ids)
            filtered_marketplaces = [
                mp for mp in active_marketplaces if mp.id in id_set
            ]
            missing_ids = id_set - {mp.id for mp in filtered_marketplaces}
            if missing_ids:
                raise HTTPException(
                    status_code=404,
                    detail=f"Marketplace(s) with ID(s) {missing_ids} not found",
                )
        else:
            filtered_marketplaces = active_marketplaces

        # Створити запит на скрапінг
        scrape_req = await self.repo_scraping.add_scrape_request(
            product_name=config.product_name
        )

        scrape_results: List[ScrapingResultSuccess | ScrapingResultError] = []

        # Обробити кожен маркетплейс
        for mp in filtered_marketplaces:
            now_utc = datetime.now(timezone.utc)
            try:
                title, price, link = await scrape_product_data(
                    marketplace=mp, product_name=config.product_name
                )
                currency = None
                if price:
                    found = re.search(r"([^\d.,\s]+)", price)
                    currency = found.group(1) if found else None

                result = ScrapingResultSuccess(
                    marketplace_name=mp.name,
                    status="success",
                    product_title=title,
                    price=price,
                    url=link,
                    scraped_at=now_utc,
                )
                scrape_results.append(result)

                await self.repo_scraping.add_scraped_product(
                    product_info=ScrapedProductCreate(
                        request_id=scrape_req.id,
                        marketplace_id=mp.id,
                        scraped_product_title=title,
                        scraped_price=price,
                        scraped_currency=currency,
                        product_url=link,
                        status="success",
                        error_message=None,
                    )
                )
            except RuntimeError as exc:
                err_msg = str(exc)
                if "Product not found" in err_msg:
                    err_status = "not_found"
                elif "Invalid selector" in err_msg:
                    err_status = "invalid_selector"
                elif "Site unavailable" in err_msg:
                    err_status = "site_unavailable"
                else:
                    err_status = "error_scraping"

                error_result = ScrapingResultError(
                    marketplace_name=mp.name,
                    status=err_status,
                    error_message=err_msg,
                    scraped_at=now_utc,
                )
                scrape_results.append(error_result)

                await self.repo_scraping.add_scraped_product(
                    product_info=ScrapedProductCreate(
                        request_id=scrape_req.id,
                        marketplace_id=mp.id,
                        scraped_product_title=config.product_name,
                        scraped_price=None,
                        scraped_currency=None,
                        product_url=None,
                        status=err_status,
                        error_message=err_msg,
                    )
                )

        # Підрахунок результатів
        summary = Summary(
            total_marketplaces_processed=len(scrape_results),
            successful_scrapes=len(
                [r for r in scrape_results if isinstance(r, ScrapingResultSuccess)]
            ),
            failed_scrapes=len(
                [r for r in scrape_results if isinstance(r, ScrapingResultError)]
            ),
        )

        return ScrapingResults(
            scrape_request_id=scrape_req.id,
            product_name_searched=config.product_name,
            results=scrape_results,
            summary=summary,
        )


def get_scraping_service(
    repo_marketplace: MarketplaceRepositoryDependency,
    repo_scraping: ScrapingRepositoryDependency,
):
    return ScrapingService(
        repo_marketplace=repo_marketplace, repo_scraping=repo_scraping
    )


ScrapingServiceDependency = Annotated[ScrapingService, Depends(get_scraping_service)]
