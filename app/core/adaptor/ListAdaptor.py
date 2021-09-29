from typing import Type

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from app.core.database_engine.db_core import get_db
from app.core.table_class import HasIdTable


class ListAdaptor:
    def __init__(self, page_index: int, page_size: int, db: Session = Depends(get_db)):
        self.page_index = page_index
        self.page_size = page_size
        self.__db = db

    def search(self, table_class: Type[HasIdTable]) -> dict:
        count = self.__db.query(func.count(table_class.id)).scalar()
        data = self.__db.query(table_class).offset((self.page_index - 1) * self.page_size) \
            .limit(self.page_size).all()
        return {
            'data': data,
            'all_count': count,
            'page_size': self.page_size,
            'page_index': self.page_index
        }

    def filter_by(self, table_class: Type[HasIdTable], condition):
        """
            :condition
                条件:
                例, HasIdTable.id < 10
        """
        count = self.__db.query(func.count(table_class.id)) \
            .get_filters(condition) \
            .scalar()
        data = self.__db.query(table_class) \
            .get_filters(condition) \
            .offset((self.page_index - 1) * self.page_size) \
            .limit(self.page_size).all()
        return {
            'data': data,
            'all_count': count,
            'page_size': self.page_size,
            'page_index': self.page_index
        }
