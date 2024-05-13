from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import Database
from models import User, Item
from serializers import CreateUserRequest, UpdateUserRequest, ItemCreateRequest, ItemUpdateRequest, CreateUserResponse

app = FastAPI()

database = Database()


@app.on_event("startup")
async def startup():
    await database.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.post("/users/", response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, db: AsyncSession = Depends(database.get_db)):
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.get("/users/")
async def read_users(db: AsyncSession = Depends(database.get_db)):
    stmt = select(User).options(selectinload(User.items))
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    stmt = select(User).filter(User.id == user_id).options(selectinload(User.items))
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UpdateUserRequest)
async def update_user(user_id: int, user_data: UpdateUserRequest, db: AsyncSession = Depends(database.get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict().items():
        if value:
            setattr(user, key, value)
            continue

    await db.commit()
    await db.refresh(user)

    return user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully"}


@app.post("/items/", response_model=ItemCreateRequest)
async def create_item(item: ItemCreateRequest, db: AsyncSession = Depends(database.get_db)):
    owner = await db.get(User, item.owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    new_item = Item(**item.dict())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@app.get("/items/")
async def read_items(db: AsyncSession = Depends(database.get_db)):
    stmt = select(Item).options(selectinload(Item.owner))
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    stmt = select(Item).filter(Item.id == item_id).options(selectinload(Item.owner))
    result = await db.execute(stmt)
    item = result.scalars().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemUpdateRequest)
async def update_item(item_id: int, item_data: ItemUpdateRequest, db: AsyncSession = Depends(database.get_db)):
    db_item = await db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    owner = await db.get(User, item_data.owner_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    for key, value in item_data.dict().items():
        if value:
            setattr(db_item, key, value)
            continue

    await db.commit()
    await db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(database.get_db)):
    db_item = await db.get(Item, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted successfully"}
