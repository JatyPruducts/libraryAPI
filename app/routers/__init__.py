from .books import router as books_router
from .authors import router as authors_router
from .users import router as users_router
from .lendings import router as lendings_router

__all__ = ["books_router", "authors_router", "users_router", "lendings_router"]
