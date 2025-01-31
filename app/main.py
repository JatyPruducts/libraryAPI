from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books_router, authors_router, users_router, lendings_router, login_router
from app.utils.logging import init_logging
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Library Management API")


# Подключение роутеров
app.include_router(books_router, prefix="/api")
app.include_router(authors_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(lendings_router, prefix="/api")
app.include_router(login_router, prefix="/api")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Инициализация логирования
init_logging()


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)