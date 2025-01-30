from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Определение ассоциативной таблицы для связи "многие ко многим"
book_authors = Table('book_authors', Base.metadata,
                     Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
                     Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
                     )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    publication_date = Column(Date)
    genre = Column(String)
    available_copies = Column(Integer)

    # Связь "многие ко многим" с авторами
    authors = relationship("Author", secondary=book_authors, back_populates="books")

    # Связь "один ко многим" с выдачами книг
    lendings = relationship("Lending", back_populates="book")
