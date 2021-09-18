from typing import TypeVar, Generic

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database_engine.db_core import get_db
from app.core.table_class import HasIdTable, DateCreateTable, DateCreateUpdateTable

T = TypeVar('T', bound=HasIdTable)


class DbAdaptor(Generic[T]):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def add(self, data_element: T, is_commit: bool = True) -> dict:
        if isinstance(data_element, DateCreateTable):
            data_element.create_stamp()
        self.db.add(data_element)
        if is_commit:
            self.db.commit()
        return data_element.get_dict()

    def read_by_id(self, id: int) -> T:
        rt: T = self.db.query(T).filter_by(id=id).first()
        return rt

    def read_all(self) -> list:
        return self.db.query(T).all()

    def update(self, data_element: T) -> dict:
        if isinstance(data_element, DateCreateUpdateTable):
            data_element.update_stamp()
        self.db.commit()
        return data_element.get_dict()

    def delete(self,id:int) -> dict:
        ...

