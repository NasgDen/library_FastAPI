from fastapi import FastAPI
from app.routers import news, users

app = FastAPI(
    title="API для сайта библиотекарей"
)

app.include_router(news.router)
app.include_router(users.router)

@app.get("/")
async def wellcome():
    return {"message": "Добро пожаловать на сайт"}