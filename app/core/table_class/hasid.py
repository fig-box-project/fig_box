from app.core.database_engine.db_core import Base
from sqlalchemy import Integer, Column


# 所有表的基类
class HasIdTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def get_dict(self):
        rt = {}
        for column in self.__table__.columns:
            rt[column.name] = str(getattr(self, column.name))
        return rt
