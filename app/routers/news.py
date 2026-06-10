from fastapi import APIRouter, status
from app.schemas import CreateNews, News

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/", response_model=News, status_code=status.HTTP_200_OK)
async def get_news():
    """
    Получение всех новостей
    """

@router.get("/{news_id}")
async def get_news_id(news_id: int):
    """
    Получение одной новости
    """

@router.post("/")
async def create_news():
    """
    Создание новости
    """
    ...

@router.put("/{news_id}")
async def change_news(news_id: int):
    """
    Редактирование новости
    """
    ...

@router.delete("/{news_id}")
async def delete_news(news_id: int):
    """
    Удаление новости
    """
    ...