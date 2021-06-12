from typing import Optional

import jwt
from fastapi import Header, HTTPException

from app.models.mdl.database import SessionLocal
from app.models.module import AuthItem
from app.models.settings.crud import settings
from app.models.user import UserMdl


class AuthFilter:
    def __init__(self, auth: AuthItem = None):
        self.auth = auth

    def ca_user(self, token: Optional[str] = Header(None)) -> UserMdl:
        # 在测试模式时总是进入管理员
        with SessionLocal() as db:
            if settings.value['auth_test_mode']:
                user_o = db.query(UserMdl).filter(
                    UserMdl.id == 1).first()
                return user_o
            # 否则检查token合法性
            else:
                user_id = jwt.decode(token,
                                     settings.value['token_key'],
                                     algorithms=['HS256'])['id']
                return db.query(UserMdl).filter_by(id=user_id).first()
