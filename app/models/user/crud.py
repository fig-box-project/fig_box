from sqlalchemy.orm import Session, load_only
from . import mdl, orm

def get_user(db: Session, id: int):
    return db.query(mdl.User).filter(mdl.User.id == id).first()

# offset 是跳过多少条的意思,可以用来翻页用
def get_users(db: Session,skip=0,limit=100):
    fields = ['id','username','character_id']
    return db.query(mdl.User).options(load_only(*fields)).offset(skip).limit(limit).all()

# 检查是否已注册
def isloged_user(db: Session,username:str):
    if db.query(mdl.User).filter_by(username=username).first() is not None:
        return True # 已注册
    else:
        return False # 未注册

# 注册
def create_user(db: Session,user: orm.UserCreate):
    db_user = mdl.User(username=user.username)
    db_user.hash_password(user.password)
    db_user.character_id = 2 # normal
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 登录
def login_user(db: Session,user_data: orm.UserCreate):
    user = db.query(mdl.User).filter_by(username=user_data.username).first()
    if not user:
        return False,"找不到用户"
    elif user.verify_password(user_data.password):
        return True,user.get_token()
    else:
        return False,"密码不匹配"

# 更新用户权限
def update_user_character(db: Session,user: orm.UserUpdate):
    # 当权限能操纵用户时
    usr = db.query(mdl.User).filter(mdl.User.id == user.id).update(
        {'character_id':user.character_id}
    )
    db.commit()
    return usr

