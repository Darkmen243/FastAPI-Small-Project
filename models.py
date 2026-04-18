from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

order_items = Table(
    'order_items',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'),primary_key=True),
    Column('item_id', Integer, ForeignKey('items.id'),primary_key=True),
    Column('quantity', Integer, default=1),
)
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    cost = Column(Float)
    orders = relationship("Order",secondary=order_items, back_populates="items")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    total_cost = Column(Float, default=0.0)
    items = relationship("Item", secondary=order_items, back_populates="orders")
    order_items = relationship("order_items", cascade="all, delete-orphan")
    
