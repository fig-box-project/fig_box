from fastapi import APIRouter, HTTPException, Depends,Header
from app.models import database
from sqlalchemy.orm import Session
from . import crud

bp = APIRouter()

@bp.get('/create_sitemap')
def create_sitemap(db: Session=Depends(database.get_db),):
    crud.SiteMap().create_sitemap(db)