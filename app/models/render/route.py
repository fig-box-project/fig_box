from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, cache
from app.main import check_token
from app.models.user.mdl import User
from fastapi.templating import Jinja2Templates
from app.models.settings.crud import settings

# 加载图库的模组
from app.models.photo import crud as photo_crud

from sqlalchemy.orm import Session
from app.models import database

templates_path = "files/templates"
templates = Jinja2Templates(directory=templates_path)

bp = APIRouter()

# 渲染图片
@bp.get("/photo/{name}")
def photo(name: str):
    return crud.read(name)

# 模版功能
@bp.get('/testa/{p:path}')
def render_test(request: Request,p:str):
    return crud.render_test(request,p)

@bp.get('/cache_test')
def cache_test():
    cache.cache.get_article(1)
    return cache.cache.get_article(2)

# 渲染列表页
@bp.get('/articles/{page}')
def list_render(page:int,request: Request,db: Session=Depends(database.get_db)):
    return crud.view_list(db,request)

@bp.get('/articleo/{link}',description='对于文章的渲染')
def render_article(link:str,request: Request,db: Session=Depends(database.get_db)):
    rt = crud.view_article(link,db,request)
    if rt != None:
        return rt

@bp.get('/site/sitemap.xml')
def site_sitemap():
    return crud.render_sitemap()

@bp.get('/site/create/sitemap')
def create_sitemap(db: Session=Depends(database.get_db)):
    crud.create_sitemap(db)

# 从settings读取数据并设置侦听
# from app.insmodes.article.rander import pull as article_pull
# @bp.get('/article/{link}', description='aaa')
# def article_page(link, request: Request, db: Session=Depends(database.get_db)):
#     return article_pull.page(db,request,templates,link)

# 获取渲染设置
rander_settings = settings.value["render"]
for k,v in rander_settings.items():
    # 从settings读取数据并设置侦听
    exec(f"from app.insmodes.{k} import render as {k}_render")
    for kp,vp in v["funs"].items():
        # 获得链接参数
        link_para = vp["link_para"]
        link_url_path = ''.join(['/{' + x + '}' for x in link_para])

        # 获得quary参数
        query_para = vp["query_para"]
        fun_para = ', '.join(link_para + query_para + ["request: Request", "db: Session=Depends(database.get_db)"])
        into_fun_para = ', '.join(['db','request','templates'] + link_para + query_para)
        # 编个执行字符
        route_code = \
f"""@bp.get('{v["prefix"]}{vp["prefix"]}{link_url_path}', description='{vp["description"]}')
def {k}_{kp}({fun_para}):
    return {k}_render.{kp}({into_fun_para})
"""
        exec(route_code) 
