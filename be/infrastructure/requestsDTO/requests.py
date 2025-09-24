from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

class AddToCartRequestDTO(BaseModel):
    product_id: int
    quantity: int




