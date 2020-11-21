from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class Article(Base):
    __tablename__ = "articles"
    id                 = Column(Integer, primary_key=True)
    title              = Column(String(64), index=True)
    content            = Column(String)

    seo_meta           = Column(String(200))
    seo_title          = Column(String(40))
    seo_keywords       = Column(String(256))
    seo_description    = Column(String(400))


    owner_id           = Column(Integer,ForeignKey('users.id'))
    owner              = relationship("User",back_populates = "articles")