from sqlalchemy.orm import Session
from app.models.user.mdl import User
from app.models.tree.crud import id_to_name
from . import mdl, orm
from datetime import datetime
import random
import app.conf as conf

# 插入category_name到文章数据里
def return_filter(article,db: Session):
    # 将图片名称转换为一个对象
    if article.image is not None:
        article.image = {"name":article.image, "url":conf.domain_port + "/photo/" + article.image}
    else:
        article.image = {"name":"", "url":""}
    # 增加个分类名称的字段
    article.category_name = id_to_name(db, article.category_id)
    return article

# 读取一个页面
def read_one_page(db: Session, id: int):
    rt = db.query(mdl.Article).filter(mdl.Article.id == id).first()
    return return_filter(rt,db)

# 渲染用,用link读取一个页面
def read_page_by_link(db: Session,link: str):
    article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
    if article is not None:
        return article
    else:
        raise Exception("搜索文章时找不到连接为:{}的文章".format(link))

# 获取用户id
def get_owner_id(db: Session, id: int):
    return db.query(mdl.Article).filter(mdl.Article.id == id).first().owner_id

# 管理员获取所有文章
def get_all_articles(db: Session, skip = 0, limit=100):
    rt = db.query(mdl.Article).offset(skip).limit(limit).all()
    rt = [return_filter(x,db) for x in rt]
    return rt

# 获取文章
def get_user_articles(db: Session,user: User,status:int, skip = 0, limit=100):
    articles = db.query(mdl.Article).filter(mdl.Article.owner_id == user.id).all()
    if status == 10:
        return [return_filter(i,db) for i in articles if i.status != -1]
    else:
        return [return_filter(i,db) for i in articles if i.status == status]


def create(db: Session,data: orm.ArticleCreate,owner_id):
    # 对map进行预操作,以对应是否发布
    data_map:dict = data.dict()
    data_map['link'] = 'gg' + str(random.randint(0,100))
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
    # 改用id作为连接
    new_Article.link = str(new_Article.id)
    db.commit()
    return {"id": new_Article.id}

def update(db: Session, data: orm.ArticleUpdate):
    new_data = data.dict()
    if data.link == None:
        del new_data["link"]
    # 增加一个更新时间戳来更新数据库
    new_data["update_date"] = datetime.now()
    db.query(mdl.Article).filter(mdl.Article.id == data.id).update(new_data)
    db.commit()
    return True

# 发布
def release(db: Session, article:orm.ArticleRelease):
    db.query(mdl.Article).filter(mdl.Article.id == article.id).update({"status":2 if article.can_search else 3})
    db.commit()
    return article.id

# 将文章转回草稿,无论是垃圾箱还是已发布
def return_to_outline(db: Session,id: int):
    # 注意此处bug,可能被利用与恢复已完全删除的文件
    db.query(mdl.Article).filter(mdl.Article.id == id).update({"status":1})
    db.commit()
    return id

def delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":0})
    db.commit()
    return article_id

def real_delete(db: Session, article_id: int):
    db.query(mdl.Article).filter(mdl.Article.id == article_id).update({"status":-1})
    db.commit()
    return article_id