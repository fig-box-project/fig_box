from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class Authority(Base):
    __tablename__ = "authoritys"
    id                    = Column(Integer, primary_key=True)
    name                  = Column(String(64))
    module                = Column(String(64))
    description           = Column(String())

class Character(Base):
    __tablename__ = "characters"
    id                    = Column(Integer, primary_key=True)
    name                  = Column(String(64))
    auths                 = Column(String())