import jwt
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Header, HTTPException
from app.models.settings.crud import settings
from app.models.user import mdl as user


class Token():
    __db: Session = None

    def set_db(self, db: Session):
        self.__db = db

    def get_token_func(self):
        if self.__db is not None:
            return self.check_token

    def check_token(self, token: Optional[str] = Header(None)):
        # 在测试模式时总是进入管理员
        if settings.value['auth_test_mode']:
            user_o = self.__db.query(user.User).filter(
                user.User.id == 1).first()
            return user_o
        # 否则检查token合法性
        else:
            user_id = self.verify_token(token)
            if user_id == None:
                raise HTTPException(status_code=400, detail='token error')
            else:
                return self.__db.query(user.User).filter_by(id=user_id).first()

    def verify_token(self, token):
        try:
            data = jwt.decode(
                token, settings.value['token_key'], algorithms=['HS256'])
        except:
            return None
        return data['id']


token = Token()

# 4/19
# def run(db: Session):
#     # 进入路由时检测token
#     # 通过在路由函数中加入这个开启验证并获得用户: now_user:User = Depends(check_token)
#     def check_token(token: Optional[str] = Header(None)):
#         # 在测试模式时总是进入管理员
#         if settings.value['auth_test_mode']:
#             user_o = db.query(user.User).filter(user.User.id == 1).first()
#             return user_o
#         # 否则检查token合法性
#         else:
#             user_id = verify_token(token)
#             if user_id == None:
#                 raise HTTPException(status_code=400, detail='token error')
#             else:
#                 return db.query(user.User).filter_by(id=user_id).first()

#     # 验证token
#     def verify_token(token):
#         try:
#             data = jwt.decode(
#                 token, settings.value['token_key'], algorithms=['HS256'])
#         except:
#             return None
#         return data['id']

#     return check_token
