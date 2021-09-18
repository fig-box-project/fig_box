from datetime import datetime

from sqlalchemy import Column, DateTime

from app.core.table_class import HasIdTable


class DateCreateTable(HasIdTable):
    __abstract__ = True
    create_date = Column(DateTime)

    def create_stamp(self):
        now = datetime.now()
        self.create_date = now
        return self


class DateCreateUpdateTable(DateCreateTable):
    """can memo when data created and when data updated"""
    __abstract__ = True
    update_date = Column(DateTime)

    def create_stamp(self):
        now = datetime.now()
        self.create_date = now
        self.update_date = now

    def update_stamp(self):
        self.update_date = datetime.now()
