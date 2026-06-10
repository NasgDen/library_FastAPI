from fastapi import FastAPI
from app.routers.news import router

app = FastAPI(
    title="API для сайта библиотекарей"
)

app.include_router(router)

@app.get("/")
async def wellcome():
    return {"message": "Добро пожаловать на сайт"}