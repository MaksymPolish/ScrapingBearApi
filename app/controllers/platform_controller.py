from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.platform import crud_platform
from app.schemas.platform import Platform, PlatformCreate, PlatformUpdate

router = APIRouter()

@router.post("/", response_model=Platform)
def create_platform(
    platform_in: PlatformCreate,
    db: Session = Depends(get_db)
):
    return crud_platform.create(db=db, obj_in=platform_in)

@router.get("/", response_model=list[Platform])
def read_platforms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_platform.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{platform_id}", response_model=Platform)
def read_platform(
    platform_id: int,
    db: Session = Depends(get_db)
):
    platform = crud_platform.get(db=db, id=platform_id)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform

@router.put("/{platform_id}", response_model=Platform)
def update_platform(
    platform_id: int,
    platform_in: PlatformUpdate,
    db: Session = Depends(get_db)
):
    platform = crud_platform.get(db=db, id=platform_id)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return crud_platform.update(db=db, db_obj=platform, obj_in=platform_in)

@router.delete("/{platform_id}", response_model=Platform)
def delete_platform(
    platform_id: int,
    db: Session = Depends(get_db)
):
    platform = crud_platform.get(db=db, id=platform_id)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return crud_platform.remove(db=db, id=platform_id)
