from datetime import datetime

from pydantic import BaseModel, Field

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
    created_at: datetime = Field(..., description="Дата и время создания новости")
    updated_at: datetime = Field(..., description="Дата и время изменения новости")