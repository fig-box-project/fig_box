from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.database import Base

class Category(Base):
    __tablename__ = 'category'
    id                 = Column(Integer, primary_key=True)
    father_ids         = Column(String)
    
    link               = Column(String, unique=False,index=True) # unique要改True
    title              = Column(String(64), index=True)
    content            = Column(String)

    create_date        = Column(DateTime)
    update_date        = Column(DateTime)
    status             = Column(Integer, default=1)# 0不可见 1可见

    description        = Column(String(200))
    seo_title          = Column(String(40))
    seo_keywords       = Column(String(256))
    seo_description    = Column(String(400))

    # owner_id           = Column(Integer,ForeignKey('users.id'),default=0)