from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.config import settings

# Загрузка переменных окружения из .env файла
load_dotenv()

# Определение базового класса для всех моделей
Base = declarative_base()

# Настройка подключения к основной базе данных
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Настройка подключения к тестовой базе данных
TEST_DATABASE_URL = settings.TEST_DATABASE_URL


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
