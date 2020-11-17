from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Character(Base):
    __tablename__ = "characters"
    id                 = Column(Integer, primary_key=True)
    name               = Column(String(64), index=True)
    can_edit_auth      = Column(Boolean, default=False)
    can_edit_tree      = Column(Boolean, default=False)
    can_edit_article   = Column(Boolean, default=True)

    users = relationship("User",back_populates='character')