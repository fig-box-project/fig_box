from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud
from app.main import check_token
from app.models.user.mdl import User

from sqlalchemy.orm import Session
from app.models import database
bp = APIRouter()

# 模版功能
@bp.get('/test/{p:path}')
def render_test(request: Request,p:str):
    return crud.render_test(request,p)

@bp.get('/article/{link}')
def render_article(link:str,request: Request,db: Session=Depends(database.get_db)):
    return crud.view_article(link,db,request)

@bp.get('/site/sitemap.xml')
def site_sitemap():
    return crud.render_sitemap()

@bp.get('/site/create/sitemap')
def create_sitemap(db: Session=Depends(database.get_db)):
    crud.create_sitemap(db)