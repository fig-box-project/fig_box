from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.database import Base

class Fmod(Base):
    __tablename__ = 'fmod'
    id                 = Column(Integer, primary_key=True)
    name               = Column(String, unique = True)