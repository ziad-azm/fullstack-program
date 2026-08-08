from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[bool] = None


class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    created_at: datetime
