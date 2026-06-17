from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import hash_password
from app.schemas import UserCreate, User as UserSchema
from app.models.users import User as UserModel
from app.db_depends import get_async_db

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=list[UserSchema], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех пользователей
    """
    result_news = await db.scalars(
        select(UserModel).where(UserModel.is_active == True)
    )
    users = result_news.all()
    return users

@router.get("/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение информации об пользователе
    """
    result_user = await db.scalars(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active == True)
    )
    user = result_user.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователя с id={user_id} не найдена")
    return user

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Создание пользователя
    """
    db_user = UserModel(
        user_name=user.user_name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def change_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Редактирование пользователя
    """
    result = await db.scalars(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active == True)
    )
    db_user = result.first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id={user_id} не найден")

    await db.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(**user.model_dump())
    )
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db:AsyncSession = Depends(get_async_db)):
    """
    Удаление новости
    """
    result = await db.scalars(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active == True)
    )
    db_user = result.first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id={user_id} не найден")

    db_user.is_active = False
    await db.commit()
    return {"message": f"Пользователь {db_user.user_name} с ID={user_id} удален"}