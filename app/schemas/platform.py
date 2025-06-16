from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PlatformBase(BaseModel):
    name: str
    search_url_template: str

class PlatformCreate(PlatformBase):
    pass

class PlatformUpdate(PlatformBase):
    pass

class Platform(PlatformBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
