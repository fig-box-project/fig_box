from fastapi import APIRouter
from app.models.page.crud import Page

bp = APIRouter()
p = Page()


@bp.get('/')
@p.wrap(is_constant=True)
def homepage(db):
    return "homepage.html", {}
