from fastapi import Depends, HTTPException
from sqlalchemy import select
from typing import Annotated, List
from db import SessionContext
from models.marketplace import Marketplace
from schemas.marketplace import MarketplaceCreateUpdate
from sqlalchemy.exc import IntegrityError


class MarketplaceRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_marketplace(self, marketplace_id: int) -> Marketplace:
        query = select(Marketplace).filter_by(id=marketplace_id)
        response = await self.session.execute(query)
        obj = response.scalar()
        if obj is None:
            raise HTTPException(status_code=404, detail="Marketplace not found")
        return obj

    async def get_all_active_marketplaces(self) -> List[Marketplace]:
        query = select(Marketplace).filter(Marketplace.is_active.is_(True))
        response = await self.session.execute(query)
        items = response.scalars()
        return [item for item in items]

    async def get_all_marketplaces(self) -> List[Marketplace]:
        query = select(Marketplace)
        response = await self.session.execute(query)
        return [market for market in response.scalars()]

    async def create_marketplace(
        self, marketplace: MarketplaceCreateUpdate
    ) -> Marketplace:
        try:
            new_marketplace = Marketplace(**marketplace.model_dump())
            self.session.add(new_marketplace)
            await self.session.commit()
            await self.session.refresh(new_marketplace)
            return new_marketplace

        except IntegrityError as e:
            await self.session.rollback()
            original_error = e.orig
            raise HTTPException(status_code=400, detail=str(original_error))
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update_marketplace(
        self, marketplace_id: int, marketplace: MarketplaceCreateUpdate
    ) -> Marketplace:
        try:
            result = await self.session.execute(
                select(Marketplace).where(Marketplace.id == marketplace_id)
            )
            existing_marketplace = result.scalar_one_or_none()
            if not existing_marketplace:
                raise HTTPException(status_code=404, detail="Marketplace id not found")

            update_data = marketplace.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_marketplace, key, value)

            await self.session.commit()
            await self.session.refresh(existing_marketplace)
            return existing_marketplace

        except IntegrityError as e:
            await self.session.rollback()
            original_error = e.orig
            raise HTTPException(status_code=400, detail=str(original_error))
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_marketplace(self, marketplace_id: int) -> None:
        marketplace_obj = await self.get_marketplace(marketplace_id)
        try:
            await self.session.delete(marketplace_obj)
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to delete marketplace: {exc}"
            )


MarketplaceRepositoryDependency = Annotated[
    MarketplaceRepository, Depends(MarketplaceRepository)
]
