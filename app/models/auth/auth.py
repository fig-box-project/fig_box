from typing import Optional

import jwt
from fastapi import Header, HTTPException

from app.models.mdl.database import SessionLocal
from app.models.module import AuthItem
from app.models.settings.crud import settings
from app.models.user import UserMdl


class AuthFilter:
    """权限的过滤器,在depend中放入该过滤器就可以自动过滤权限"""

    def __init__(self, auth: AuthItem = None):
        self.auth = auth

    def ca(self, token: Optional[str] = Header(None)) -> UserMdl:
        with SessionLocal() as db:
            # 在测试模式时总是进入管理员
            if settings.value['auth_test_mode']:
                user_o = db.query(UserMdl).filter(
                    UserMdl.id == 1).first()
                rt: UserMdl = user_o
            # 否则检查token合法性
            else:
                user_id = jwt.decode(token,
                                     settings.value['token_key'],
                                     algorithms=['HS256'])['id']
                rt: UserMdl = db.query(UserMdl).filter_by(id=user_id).first()
            rt.character
