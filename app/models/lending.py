from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Lending(Base):
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    lend_date = Column(Date)
    return_date = Column(Date)

    # Добавляем обратные связи к user и book
    user = relationship("User", back_populates="lendings")
    book = relationship("Book", back_populates="lendings")
