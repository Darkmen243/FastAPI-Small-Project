from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import models
import schemas


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User).where(models.User.id==user_id)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    update_data = user_update.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(
            update(models.User)
            .where(models.User.id==user_id)
            .values(**update_data)
        )
        await db.commit()
    return await get_user(db,user_id)


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        delete(models.User).where(models.User.id==user_id)
    )
    await db.commit()
    return result.rowcount>0

async def get_users(db:AsyncSession,skip:int=0,limit:int =100):
   result = await db.execute(
       select(models.User).offset(skip).limit(limit)
   )
   return result.scalars().all()

async def create_item(db:AsyncSession, item:schemas.ItemCreate):
    db_item = models.Item(name=item.name, cost=item.cost)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

async def get_item(db:AsyncSession,item_id:int):
    result = await db.execute(
        select(models.Item).where(models.Item.id==item_id)
    )
    return result.scalar_one_or_none()

async def get_items(db:AsyncSession, skip:int=0, limit:int=100):
    result = await db.execute(
        select(models.Item).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_item(db:AsyncSession, item_id:int, item_update: schemas.ItemUpdate):
    update_data = item_update.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(
            update(models.Item)
            .where(models.Item.id==item_id)
            .values(**update_data)
        )
        await db.commit()
    return await get_user(db,item_id)

async def get_order_with_items(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order)
        .where(models.Order.id == order_id)
        .options(selectinload(models.Order.items))  # Eager loading
    )
    return result.scalar_one_or_none()

async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(name=order.name, total_cost=0.0)
    db.add(db_order)
    await db.flush()  # Get ID without committing
    total_cost = 0.0
    for order_item in order.items:
        result = await db.execute(
            select(models.Item).where(models.Item.id == order_item.item_id)
        )
        item = result.scalar_one_or_none()
        
        if item:
            total_cost += item.cost * order_item.quantity
            await db.execute(
                models.order_items.insert().values(
                    order_id=db_order.id,
                    item_id=item.id,
                    quantity=order_item.quantity
                )
            )
    
    db_order.total_cost = total_cost
    await db.commit()
    await db.refresh(db_order)
    
    return db_order

