from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.mdl.page import PageMdl


class Category(PageMdl):
    __tablename__ = 'category'
    # 暂时无用
    father_id = Column(String)
