from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict

class CreateNews(BaseModel):
    """
    Класс для валидации полей для созданния, изменения новости
    """
    title: str = Field(..., min_length=3, max_length=100, description="Название новости")
    content: str = Field(..., description="Содержание новости")

class News(BaseModel):
    """
    Класс для валидации полей для модели новостей
    """
    id: int = Field(..., description="ID новости")
    title: str = Field(..., min_length=3, max_length=100, description="Название новости")
    content: str = Field(..., description="Содержание новости")
    is_active: bool = Field(..., description="Активная новость")
    created_at: datetime = Field(..., description="Дата и время создания новости")
    updated_at: datetime = Field(..., description="Дата и время изменения новости")

class UserCreate(BaseModel):
    """
    Класс для валидации полей для создания, изменения модели пользователь
    """
    user_name:str = Field(..., min_length=3, max_length=20, description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    password: str = Field(..., description="Пароль пользователя")

    model_config = ConfigDict(from_attributes=True)

class User(UserCreate):
    """
    Класс для валидации полей для модели пользователь
    """
    id: int = Field(..., description="ID пользователя")
    is_active: bool = Field(..., description="Активный пользователь")
    created_at: datetime = Field(..., description="Дата и время создания пользователя")
    updated_at: datetime = Field(..., description="Дата и время изменения пользователя")
