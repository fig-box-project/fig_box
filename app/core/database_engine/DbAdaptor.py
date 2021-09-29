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
        """データを追加する"""
        if isinstance(data_element, DateCreateTable):
            data_element.create_stamp()
        self.db.add(data_element)
        if is_commit:
            self.db.commit()
        return data_element.get_dict()

    def read_by_id(self, id: int) -> HasIdTable:
        """IDを使ってデータを読み出す"""
        rt = self.db.query(self.TbClass).filter_by(id=id).first()
        return rt

    def read_by(self, **kwargs) -> HasIdTable:
        """簡単なイコール条件を使ってデータを読み出す"""
        rt = self.db.query(self.TbClass).filter_by(**kwargs).first()
        return rt

    def read_all(self) -> list:
        """データベースの全部を取る"""
        return self.db.query(self.TbClass).all()

    def update(self, data_element: HasIdTable, is_commit: bool = True) -> dict:
        """エレメントでデータを更新する
            :data_element
                [read_...]を使ってこのエレメントを獲得
            :is_commit
                これをFalseに変えたらコミットはしない
                最後の変更処理ではない時はFalseにする
        """
        if isinstance(data_element, DateCreateUpdateTable):
            data_element.update_stamp()
        if is_commit:
            self.db.commit()
        return data_element.get_dict()

    def delete(self, id: int) -> dict:
        """IDでデータを削除する"""
        count = self.db.query(self.TbClass).filter_by(id=id).delete()
        return {'count': count}

    def delete_by(self, **kwargs) -> dict:
        """指定した条件でデータを削除する"""
        count = self.db.query(self.TbClass).filter_by(**kwargs).delete()
        return {'count': count}

    def commit(self):
        """コミット、つまり変更を実際のデータベースに入れる"""
        self.db.commit()

