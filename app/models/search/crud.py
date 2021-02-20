

# 数据库搜索,
def Moudle(db, db_name, type, count, params:list):
    bigFirst = db_name.capitalize()
    lower = db_name.lower()

    # from app.insmodes.article.mdl import Article
    exec(f"from app.insmodes.{lower}.mdl import {bigFirst}")
    # 搜索同分类下文章
    if type == "same_category":
        # rt = db.query(Article).filter(Article.category_id == 0).limit(count).all()
        # print(rt)
        rt = eval(f"db.query({bigFirst}).filter({bigFirst}.category_id == params[0]).limit(count).all()")
        return rt
    else:
        return None