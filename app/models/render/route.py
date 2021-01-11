from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, cache
from app.main import check_token
from app.models.user.mdl import User

# 加载图库的模组
from app.models.photo import crud as photo_crud

from sqlalchemy.orm import Session
from app.models import database
bp = APIRouter()

# 渲染图片
@bp.get("/photo/{name}")
def photo(name: str):
    return photo_crud.read(name)

# 模版功能
@bp.get('/testa/{p:path}')
def render_test(request: Request,p:str):
    return crud.render_test(request,p)

@bp.get('/cache_test')
def cache_test():
    cache.cache.get_article(1)
    return cache.cache.get_article(2)

@bp.get('/list_test')
def list_test():
    return crud.view_list(None, None)

@bp.get('/article/{link}',description='对于文章的渲染')
def render_article(link:str,request: Request,db: Session=Depends(database.get_db)):
    rt = crud.view_article(link,db,request)
    if rt != None:
        return rt
    # else:
        # raise HTTPException(status_code=400,detail='找不到页面')



@bp.get('/site/sitemap.xml')
def site_sitemap():
    return crud.render_sitemap()

@bp.get('/site/create/sitemap')
def create_sitemap(db: Session=Depends(database.get_db)):
    crud.create_sitemap(db)