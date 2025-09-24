from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

class ProductResponseDTO(BaseModel):
    id: str
    name: str
    price: int


class CartResponseDTO(BaseModel):
    id: str
    product_id: int
    quantity: int




