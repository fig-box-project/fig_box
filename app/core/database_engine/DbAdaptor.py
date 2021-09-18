from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database_engine.db_core import get_db
from app.core.table_class import HasIdTable, DateCreateTable, DateCreateUpdateTable


class DbAdaptor:
    def __init__(self, table_class: Type[HasIdTable]):
        self.db = None
        self.TbClass = table_class

    def dba(self, db: Session = Depends(get_db)):
        self.db = db
        return self

    def add(self, data_element: HasIdTable, is_commit: bool = True) -> dict:
        if isinstance(data_element, DateCreateTable):
            data_element.create_stamp()
        self.db.add(data_element)
        if is_commit:
            self.db.commit()
        return data_element.get_dict()

    def read_by_id(self, id: int) -> HasIdTable:
        rt = self.db.query(self.TbClass).filter_by(id=id).first()
        return rt

    def read_all(self) -> list:
        return self.db.query(self.TbClass).all()

    def update(self, data_element: HasIdTable) -> dict:
        if isinstance(data_element, DateCreateUpdateTable):
            data_element.update_stamp()
        self.db.commit()
        return data_element.get_dict()

    def delete(self, id: int) -> dict:
        count = self.db.query(self.TbClass).filter_by(id=id).delete()
        return {'deleted count': count}
