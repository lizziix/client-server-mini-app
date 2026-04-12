from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0)


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, gt=0)
