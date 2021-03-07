from sqlalchemy.orm import load_only
from app.models.settings.crud import settings

# 数据库搜索,
def db_search(db, db_name:str, type, count, params:list):
    bigFirst = db_name.capitalize()
    lower = db_name.lower()

    # from app.insmodes.article.mdl import Article
    exec(f"from app.insmodes.{lower}.mdl import {bigFirst}")
    # 搜索同分类下文章
    if type == "same_category":
        # 使用此选项时:0,category_id 1,page_index
        # rt = db.query(Article).filter(Article.category_id == 0).limit(count).all()
        # print(rt)
        if len(params) == 1:
            fields = ['title','link'] # 使用中
            rt = eval(f"db.query({bigFirst}).options(load_only(*fields)).filter({bigFirst}.category_id == params[0]).limit(count).all()")
        elif len(params) == 2:
            fields = ['title', 'link', 'description']
            rt = eval(f"db.query({bigFirst}).options(load_only(*fields)).filter({bigFirst}.category_id == params[0]).limit(count).offset((int(params[0])-1)*count).all()")
        change_link_to_abs(rt)
        return rt
    else:
        return None

def change_link_to_abs(rt):
    for i in rt:
        print(type(i.link))
        i.link = settings.value["domain_port"] + "/article/show/" + str(i.link)