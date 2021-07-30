from sqlalchemy import Column, String, DateTime

from app.models.mdl import DateCreatedMdl


class TriggerMdl(DateCreatedMdl):
    __tablename__ = 'schedule_trigger'
    name = Column(String(21), index=True)
    logic = Column(String(64))
    description = Column(String(128))
    start_date = Column(DateTime)
    end_date = Column(DateTime)