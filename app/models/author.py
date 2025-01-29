from sqlalchemy import Column, Integer, String, Date, Text
from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(Text)
    date_of_birth = Column(Date)
