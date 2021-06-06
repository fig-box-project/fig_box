from sqlalchemy.orm import Session, load_only
from starlette.requests import Request

from . import mdl, orm
from ..log import LogTools, UserLogMdl


class UserCrud:

    @staticmethod
    def get_user(db: Session, id: int):
        return db.query(mdl.UserMdl).filter(mdl.UserMdl.id == id).first()

    # offset 是跳过多少条的意思,可以用来翻页用

    @staticmethod
    def get_users(db: Session, skip=0, limit=100):
        fields = ['id', 'username', 'character']
        return db.query(mdl.UserMdl).options(load_only(*fields)).offset(skip).limit(limit).all()

    @staticmethod
    def check_user_name(db: Session, username: str):
        """检查是否已注册"""
        if db.query(mdl.UserMdl).filter_by(username=username).first() is not None:
            return True  # 已注册
        else:
            return False  # 未注册

    @staticmethod
    def create_user(db: Session, user: orm.UserCreate, request: Request):
        db_user = mdl.UserMdl(username=user.username)
        db_user.hash_password(user.password)
        db_user.character = "normal"  # normal
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # log
        UserLogMdl.user_log('注册', db_user.id, request, db)
        return db_user

    @staticmethod
    def login_user(db: Session, user_data: orm.UserLogin, request:Request):
        user = db.query(mdl.UserMdl).filter_by(username=user_data.username).first()
        if not user:
            return False, "找不到用户"
        elif user.verify_password(user_data.password):
            # log
            UserLogMdl.user_log('登录', user.id, request, db)
            return True, user.get_token()
        else:
            return False, "密码不匹配"
