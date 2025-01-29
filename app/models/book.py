from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    publication_date = Column(Date)
    genre = Column(String)
    available_copies = Column(Integer)

    authors = relationship("Author", secondary="book_authors")
