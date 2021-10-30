from typing import Type, Callable

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from app.core.database_engine.db_core import get_db
from app.core.table_class import HasIdTable


class ListAdaptor:
    def __init__(self, page_index: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
        self.page_index = page_index
        self.page_size = page_size
        self.__db = db

    def search(self, table_class: Type[HasIdTable], map_filter: Callable = None) -> dict:
        """ map_filter is a function to filter all the data, it has one input and one output,
        it means old_data and new_data.
         map_filterは関数です、データベースの毎行をdirtにしてパラメータに入れる、結果（新しいdirtデータ）をリターンしてください"""
        count = self.__db.query(func.count(table_class.id)).scalar()
        data = self.__db.query(table_class).offset((self.page_index - 1) * self.page_size) \
            .limit(self.page_size).all()
        if map_filter is not None:
            old_data = data
            data = []
            for i in old_data:
                data.append(map_filter(i.get_dict()))
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
