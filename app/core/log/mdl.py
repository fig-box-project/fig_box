from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.log import LogTools
from app.core.table_class import DateCreateTable
from app.core.tools import Tools


class UserLogTable(DateCreateTable):
    __tablename__ = 'userlogs'
    user_id = Column(Integer, index=True)
    method_type = Column(String(10), index=True)
    ip = Column(String(45))
    address1 = Column(String(64))
    address2 = Column(String(64))
    user_agent = Column(String(200))

    @staticmethod
    def user_log(status: str, user_id: int,
                 request: Request, db: Session):
        """status 0 注册, 1 登录, 其它数字 其它意思"""
        ip = Tools.get_user_ip(request)
        address1, address2 = Tools.get_ip_description(ip)
        # log到数据库
        item = {'user_id': user_id,
                'method_type': status,
                'ip': ip,
                'address1': address1,
                'address2': address2,
                'user_agent': request.headers['user-agent']}
        add_item = UserLogTable(**item).create_stamp()
        db.add(add_item)
        db.commit()
        # log到文件
        LogTools.user_log(status, user_id, ip, address1, address2)
