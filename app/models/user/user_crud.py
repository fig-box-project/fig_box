from sqlalchemy.orm import Session
from .user import User as Userm
from .user_orm import *

def get_user(db: Session, id: int):
    return db.query(Userm).filter(Userm.id == id).first()

def get_users(db: Session,skip=0,limit=100):
    return db.query(Userm).offset(skip).limit(limit).all()

# 检查是否已注册
def check_user(db: Session,username:str):
    if db.query(Userm).filter_by(username=username).first() is not None:
        return True # 已注册
    else:
        return False # 未注册

# 注册
def create_user(db: Session,user: UserCreate):
    db_user = Userm(username=user.username)
    db_user.hash_password(user.password)
    db_user.character_id = 1 # normal
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 登录
def login_user(db: Session,user: UserCreate):
    user = db.query(Userm).filter_by(username=user.username).first()
    if not user:
        return "fail"
    elif user.verify_password(user.password):
        return user.get_token()
    else:
        return "非法"

# 更新用户权限
def update_user_character(db: Session,user: User,token:str):
    now_user_id = Userm.verify_token(token)
    # 当token解压成功时
    if now_user_id is not None:
        # 获得现在用户的实例
        now_user = db.query(Userm).filter(Userm.id == now_user_id).first()
        # 当权限能操纵用户时
        if now_user.character.can_edit_auth:
            user = db.query(Userm).filter(Userm.id == user.id).update(
                {'character_id':user.character_id}
            )
            db.commit()
            return 200
    return 400

