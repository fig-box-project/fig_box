from fastapi import APIRouter
from html_builder import Html
from html_builder.Body.Anchor import Anchor

from app.models.page.crud import PageRouter, RequestItem


def homepage_route(bp: APIRouter, p: PageRouter):
    def html_creator():
        rt = Html('homepage')
        rt.body.addElement(Anchor('docs').text(
            '''to the API List Page<br>
            API 可視化ページへ<br>
            转到可视化API页面'''
        ))
        return rt

    @bp.get('/')
    @p.wrap(is_constant=True)
    def homepage(db):
        # return "homepage.html", {}, html_creator
        return RequestItem('homepage.html', {}, html_creator)
