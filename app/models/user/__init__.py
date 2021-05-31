from typing import List

from requests import Session
from .mdl import UserMdl

from app.models.module import ApiModule, PageModule, PageItem, TableModule
from app.models.user.route import user_api_route, user_page_route

# 不要删
from . import mdl


class User(ApiModule, PageModule, TableModule):
    def get_table(self):
        return [UserMdl]

    def __init__(self):
        ApiModule.__init__(self)
        PageModule.__init__(self)

    def _register_api_bp(self, bp):
        user_api_route(bp)

    def _register_page_bp(self, bp, page_router):
        user_page_route(bp, page_router)

    def _get_pages(self, db: Session) -> List[PageItem]:
        # TODO
        pass

    def _get_tag(self) -> str:
        return '用户'

    def get_module_name(self) -> str:
        return 'user'


user = User()
