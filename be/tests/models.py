from dataclasses import dataclass

@dataclass
class CartItem:
    product_id: int
    quantity: int
    
    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }


@dataclass
class Product:
    id: str
    name: str
    price: int
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
