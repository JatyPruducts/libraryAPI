from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(Text)
    date_of_birth = Column(Date)

    # Связь "многие ко многим" с книгами
    books = relationship("Book", secondary="book_authors", back_populates="authors")
