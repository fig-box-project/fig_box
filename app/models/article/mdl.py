from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.database import Base

class Article(Base):
    __tablename__ = "articles"
    id                 = Column(Integer, primary_key=True)
    link               = Column(String, unique=True,index=True)
    title              = Column(String(64), index=True)
    content            = Column(String)

    create_date        = Column(DateTime)
    update_date        = Column(DateTime)
    status             = Column(Integer, default=1)# 0垃圾箱 1草稿箱 2已发布 3已发布不索引
    category_id        = Column(Integer, default=0)

    image              = Column(String)
    description        = Column(String(200))
    seo_title          = Column(String(40))
    seo_keywords       = Column(String(256))
    seo_description    = Column(String(400))

    owner_id           = Column(Integer)

    # 想在网页上显示什么内容
    # def keys(self):
    #     return ('title','link')
    # def __getitem__(self, item):
    #     return getattr(self, item)