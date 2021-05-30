from sqlalchemy import Column, Integer, String

from app.models.mdl import DateCreatedMdl


class UserLogMdl(DateCreatedMdl):
    user_id = Column(Integer, index=True)
    method_type = Column(String(10), index=True)
    ip = Column(String(45))
    address = Column(String(64))
