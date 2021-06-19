from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models.mdl import DateCUMdl, HasidMdl
from app.models.mdl.database import Base

# 用来启动多对多的数据结构的
character_auth = Table(
    "character_auth",
    Base.metadata,
    Column("character_id", Integer, ForeignKey(
        "character.id"), nullable=False, primary_key=True),
    Column("auth_id", Integer, ForeignKey("auth.id"),
           nullable=False, primary_key=True)
)


class CharacterMdl(DateCUMdl):
    """角色的数据库"""
    __tablename__ = "character"
    name = Column(String(64), index=True)

    users = relationship('UserMdl', back_populates='character')
    # 2是全部权限,1是默认权限,0是无权限
    auth_type = Column(Integer)
    auths: list = relationship('AuthMdl', secondary=character_auth)


class AuthMdl(HasidMdl):
    """权限的数据库"""
    __tablename__ = 'auth'
    # 唯一的权限名
    name = Column(String(128), index=True, unique=True)
    characters = relationship('CharacterMdl', secondary=character_auth)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name
