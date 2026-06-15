from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CreateNews, News as NewsSchema
from app.models import News as NewsModel
from app.db_depends import get_async_db

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

@router.get("/", response_model=list[NewsSchema], status_code=status.HTTP_200_OK)
async def get_news(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех новостей
    """
    result_news = await db.scalars(
        select(NewsModel).where(NewsModel.is_active == True)
    )
    news = result_news.all()
    return news

@router.get("/{news_id}", response_model=NewsSchema, status_code=status.HTTP_200_OK)
async def get_news_id(news_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение одной новости
    """
    result_news = await db.scalars(
        select(NewsModel).where(NewsModel.id == news_id, NewsModel.is_active == True)
    )
    print(result_news)
    news = result_news.first()

    if news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Новость с id={news_id} не найдена")
    return news

@router.post("/", response_model=NewsSchema, status_code=status.HTTP_201_CREATED)
async def create_news(news: CreateNews, db: AsyncSession = Depends(get_async_db)):
    """
    Создание новости
    """
    db_news =NewsModel(**news.model_dump())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

@router.put("/{news_id}", response_model=NewsSchema, status_code=status.HTTP_200_OK)
async def change_news(news_id: int, news: CreateNews, db: AsyncSession = Depends(get_async_db)):
    """
    Редактирование новости
    """
    result = await db.scalars(
        select(NewsModel).where(NewsModel.id == news_id, NewsModel.is_active == True)
    )
    db_news = result.first()
    if db_news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Новость с id={news_id} не найдена")

    await db.execute(
        update(NewsModel)
        .where(NewsModel.id == news_id)
        .values(**news.model_dump())
    )
    await db.commit()
    await db.refresh(db_news)
    return db_news


@router.delete("/{news_id}", status_code=status.HTTP_200_OK)
async def delete_news(news_id: int, db:AsyncSession = Depends(get_async_db)):
    """
    Удаление новости
    """
    result = await db.scalars(
        select(NewsModel).where(NewsModel.id == news_id, NewsModel.is_active == True)
    )
    db_news = result.first()
    if db_news is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Новость с id={news_id} не найдена")

    db_news.is_active = False
    await db.commit()
    return {"message": f"Новость с ID={news_id} удалена"}