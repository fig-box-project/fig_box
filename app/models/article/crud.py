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

# 获取文章
def get_user_articles(db: Session,user: User,status:int, skip = 0, limit=100):
    if status == 10:
        return [i for i in user.articles if i.status != -1]
    else:
        return [i for i in user.articles if i.status == status]


def create(db: Session,data: orm.ArticleCreate,owner_id):
    # 对map进行预操作,以对应是否发布
    data_map:dict = data.dict()
    if data_map.pop('is_release'):
        if data_map.pop('can_search'):
            data_map['status']=2
        else:
            data_map['status']=3
    else:
        data_map.pop('can_search')
        data_map['status']=1
    # 用map新建对象,准备创建
    new_Article = mdl.Article(**data_map)
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
    db.flush()
    db.commit()
    return True

# 发布
def release(db: Session, article:orm.ArticleRelease):
    db.query(mdl.Article).filter(mdl.Article.id == article.id).update({"status":2 if article.can_search else 3})
    db.flush()
    db.commit()
    return article.id

# 将文章转回草稿,无论是垃圾箱还是已发布
def return_to_outline(db: Session,id: int):
    # 注意此处bug,可能被利用与恢复已完全删除的文件
    db.query(mdl.Article).filter(mdl.Article.id == id).update({"status":1})
    db.flush()
    db.commit()
    return id

def delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":0})
    db.flush()
    db.commit()
    return article_id

def real_delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":-1})
    db.flush()
    db.commit()
    return article_id