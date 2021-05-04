
from fastapi import APIRouter
from html_builder import Html
from html_builder.Body.Anchor import Anchor

from app.models.page.crud import Page

bp = APIRouter()
p = Page()


def html_creator():
    rt = Html('homepage')
    rt.body.addElement(Anchor('docs').text('转到API'))
    return rt


@bp.get('/')
@p.wrap(is_constant=True)
def homepage(db):
    return "homepage.html", {}, html_creator
