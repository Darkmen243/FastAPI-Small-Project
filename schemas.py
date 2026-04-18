from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    cost: float


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    cost: Optional[float] = None


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    item_id: int
    quantity: int = 1


class OrderBase(BaseModel):
    name: str


class OrderCreate(OrderBase):
    items: List[OrderItemBase] = []


class OrderUpdate(BaseModel):
    name: Optional[str] = None
    items: Optional[List[OrderItemBase]] = None


class OrderResponse(OrderBase):
    id: int
    total_cost: float
    items: List[ItemResponse]

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    items_with_quantities: List[dict]
