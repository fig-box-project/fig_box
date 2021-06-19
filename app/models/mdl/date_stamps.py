from datetime import datetime

from sqlalchemy import Column, DateTime

from app.models.mdl import HasidMdl


class DateCreatedMdl(HasidMdl):
    __abstract__ = True
    create_date = Column(DateTime)

    def create_stamp(self):
        now = datetime.now()
        self.create_date = now
        return self


class DateCUMdl(DateCreatedMdl):
    __abstract__ = True
    update_date = Column(DateTime)

    def create_stamp(self):
        now = datetime.now()
        self.create_date = now
        self.update_date = now

    def update_stamp(self):
        self.update_date = datetime.now()
