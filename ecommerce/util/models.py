from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class User:
    username: str
    password_hash: str
    sign_up_date: str  # Consider using datetime and converting to string when interfacing with DynamoDB
    firstname: str
    lastname: str
    shopping_cart: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Company:
    registration_number: str
    company_name: str
    company_email: str
    company_background_image: str
    company_description: str


@dataclass
class Product:
    product_id: str
    category: str


@dataclass
class ProductCategory:
    category: str
    products: List[Product] = field(default_factory=list)


@dataclass
class ShoppingCartItem:
    product_id: str
    quantity: int
    # Add more fields as necessary, e.g., price, name, etc.


@dataclass
class ShoppingCart:
    username: str  # Assuming this is the identifier linking the cart to a user
    items: List[ShoppingCartItem] = field(default_factory=list)
