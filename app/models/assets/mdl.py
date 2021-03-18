from app.models.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

class Assets(Base):
    __tablename__ = "assets"
    id            = Column(Integer, primary_key=True)
    owner_id      = Column(Integer)
    create_date   = Column(DateTime)
    # 暂时无用的字段
    link          = Column(String, default = None)
    type          = Column(String, default = None)
