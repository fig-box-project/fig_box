from sqlalchemy.orm import Session
from app.models.user.user import User
from . import mdl, orm

# 读取一个页面
def read_one_page(db: Session, id: int):
    return db.query(mdl.Article).filter(mdl.Article.id == id).first()

# 获取用户id
def get_owner_id(db: Session, id: int):
    return db.query(mdl.Article).filter(mdl.Article.id == id).first().owner_id

# 获取所有
def get_all_articles(db: Session, skip = 0, limit=100):
    return db.query(mdl.Article).offset(skip).limit(limit).all()

def get_user_articles(db: Session,user: User, skip = 0, limit=100):
    return [{
        "id":i.id,
        "title":i.title,
        "description":i.description,
        "seo_title":i.seo_title,
        "seo_keywords":i.seo_keywords,
        "seo_description":i.seo_description} for i in user.articles]


def create(db: Session,data: orm.ArticleCreate,owner_id):
    new_Article = mdl.Article(**data.dict())
    new_Article.owner_id = owner_id
    db.add(new_Article)
    db.commit()
    db.refresh(new_Article)
    return new_Article

def update(db: Session, data: orm.ArticleUpdate):
    db.query(mdl.Article).filter(mdl.Article.id == data.id).update(data.dict())
    db.commit()
    return True

def delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).delete()
    # 只提交到缓存时使用flush
    db.commit()
    return article_id
