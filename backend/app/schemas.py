from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# -- Product Schemas --
class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductListResponse(BaseModel):
    items: List[Product]
    total: int
    
# -- User Schemas --
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# -- Order Schemas --
class OrderBase(BaseModel):
    user_id: int
    created_at: Optional[datetime] = None

class OrderWithUsername(BaseModel):
    id: int
    user_id: int
    username: str | None
    created_at: str  # or datetime if you prefer
    
class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

# -- Transaction Schemas --
class TransactionBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
