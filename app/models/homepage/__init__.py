from datetime import datetime
from typing import List

from app.models.homepage.page import homepage_route
from app.models.module import PageModel, PageItem


class Homepage(PageModel):
    def _register_page_bp(self, bp, page_router):
        self._page_bp.change_prefix('')
        homepage_route(bp, page_router)

    def get_pages(self) -> List[PageItem]:
        return [PageItem('/', datetime.today())]

    def _get_tag(self) -> str:
        return '首页'

    def get_module_name(self) -> str:
        return 'homepage'


homepage = Homepage()
