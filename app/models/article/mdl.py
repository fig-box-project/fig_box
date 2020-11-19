from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class Article(Base):
    __tablename__ = "articles"
    id                 = Column(Integer, primary_key=True)
    title              = Column(String(64), index=True)
    content            = Column(String)

    owner_id           = Column(Integer,ForeignKey('users.id'))
    owner              = relationship("User",back_populates = "articles")