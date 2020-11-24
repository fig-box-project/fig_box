from sqlalchemy.orm import Session
from app.models.user.user import User
from . import mdl, orm
from datetime import datetime

# 读取一个页面
def read_one_page(db: Session, id: int):
    return db.query(mdl.Article).filter(mdl.Article.id == id).first()

# 获取用户id
def get_owner_id(db: Session, id: int):
    return db.query(mdl.Article).filter(mdl.Article.id == id).first().owner_id

# 管理员获取所有文章
def get_all_articles(db: Session, skip = 0, limit=100):
    return db.query(mdl.Article).offset(skip).limit(limit).all()

# 获取草稿箱的文章
def get_user_articles(db: Session,user: User,status = 1, skip = 0, limit=100):
    return [i for i in user.articles if i.status == status]


def create(db: Session,data: orm.ArticleCreate,owner_id):
    new_Article = mdl.Article(**data.dict())
    # 创建当时的时间戳
    new_Article.create_date = datetime.now()
    new_Article.update_date = datetime.now()
    new_Article.owner_id = owner_id
    db.add(new_Article)
    db.commit()
    db.refresh(new_Article)
    return new_Article

def update(db: Session, data: orm.ArticleUpdate):
    new_data = data.dict()
    # 增加一个更新时间戳来更新数据库
    new_data["update_date"] = datetime.now()
    db.query(mdl.Article).filter(mdl.Article.id == data.id).update(new_data)
    db.commit()
    return True

def release(db: Session, article_id: int,can_search: bool=True):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":2 if can_search else 3})
    db.commit()
    return article_id

def delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":0})
    # 只提交到缓存时使用flush
    db.commit()
    return article_id
