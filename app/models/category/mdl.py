from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from app.models.mdl import PageMdl


class Category(PageMdl):
    __tablename__ = 'category'
    # 暂时无用
    father_id = Column(Integer)
