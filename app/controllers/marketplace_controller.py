from fastapi import APIRouter
from crud.marketplace_repository import MarketplaceRepositoryDependency
from schemas.marketplace import MarketplaceCreateUpdate, MarketplaceResponse

marketplace_router = APIRouter(prefix="/marketplaces", tags=["marketplaces"])


@marketplace_router.post("", response_model=MarketplaceResponse)
async def add_marketplace(
    marketplace: MarketplaceCreateUpdate, repo: MarketplaceRepositoryDependency
):
    new_marketplace = await repo.create_marketplace(marketplace)
    return MarketplaceResponse.model_validate(new_marketplace)


@marketplace_router.get("", response_model=list[MarketplaceResponse])
async def list_marketplaces(repo: MarketplaceRepositoryDependency):
    all_marketplaces = await repo.get_all_marketplaces()
    return [MarketplaceResponse.model_validate(item) for item in all_marketplaces]


@marketplace_router.get("/{marketplace_id}", response_model=MarketplaceResponse)
async def fetch_marketplace(marketplace_id: int, repo: MarketplaceRepositoryDependency):
    result = await repo.get_marketplace(marketplace_id)
    return MarketplaceResponse.model_validate(result)


@marketplace_router.put("/{marketplace_id}", response_model=MarketplaceResponse)
async def modify_marketplace(
    marketplace_id: int,
    data: MarketplaceCreateUpdate,
    repo: MarketplaceRepositoryDependency,
):
    updated = await repo.update_marketplace(marketplace_id, data)
    return MarketplaceResponse.model_validate(updated)


@marketplace_router.delete("/{marketplace_id}", status_code=204)
async def remove_marketplace(
    marketplace_id: int, repo: MarketplaceRepositoryDependency
):
    await repo.delete_marketplace(marketplace_id)
    return {"detail": "Marketplace has been removed"}
