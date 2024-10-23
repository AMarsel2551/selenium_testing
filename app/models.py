from typing import Optional
from pydantic import BaseModel


class Price(BaseModel):
    price: int
    discount: int
    final_price: int


class Product(BaseModel):
    name: str
    seller: str
    category: str
    brand: str
    sku: str
    price: Price
    photo: str
    stocks: Optional[list] = []
    rating: float
