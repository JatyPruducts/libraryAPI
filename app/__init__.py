from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books_router, authors_router, users_router, lendings_router
from app.utils.logging import init_logging
from app.config import settings
