from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

class AddToCartRequestDTO(BaseModel):
    product_id: int
    quantity: int


@dataclass
class AddToCartRequest:
    """Data class for add to cart request"""
    product_id: int
    quantity: int
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }
    


