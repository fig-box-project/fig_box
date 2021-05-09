from datetime import datetime
from typing import List

from app.models.homepage.page import homepage_route
from app.models.module import PageModule, PageItem


class Homepage(PageModule):
    def __init__(self):
        PageModule.__init__(self)
    
    def _register_page_bp(self, bp, page_router):
        self._page_bp.change_prefix('')
        homepage_route(bp, page_router)

    def get_pages(self, db) -> List[PageItem]:
        return [PageItem('/', datetime.today())]

    def _get_tag(self) -> str:
        return '首页'

    def get_module_name(self) -> str:
        return 'homepage'


homepage = Homepage()
