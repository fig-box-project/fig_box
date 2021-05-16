from typing import List

from fastapi import APIRouter
from requests.sessions import Session

from app.models.category.route import category_page_route, category_route
from app.models.module import ApiModule, PageModule, PageItem


class Category(ApiModule, PageModule):
    def _register_api_bp(self, bp: APIRouter):
        category_route(bp)

    def _register_page_bp(self, bp, page_router):
        category_page_route(bp, page_router)

    def _get_pages(self, db: Session) -> List[PageItem]:
        # TODO
        pass

    def _get_tag(self) -> str:
        return '分类'

    def get_module_name(self) -> str:
        return 'category'

    def __init__(self):
        ApiModule.__init__(self)
        PageModule.__init__(self)
