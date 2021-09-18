from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from app.core.table_class import PageTable
from app.core.module_class import BluePrintSet, RouteAbleModule
from app.core.page.crud import PageRouter


class PageItem:
    """暂时用于sitemap,如有其它用处时可扩张"""

    def __init__(self, link: str, update_date: datetime):
        self.link = link
        self.update_date = update_date


class PageModule(RouteAbleModule, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self._page_bp = BluePrintSet(
            f'/{self.get_module_name()}', self._get_tag())
        self.page_router = PageRouter()
        self._register_page_bp(self._page_bp.get_bp(), self.page_router)

    @abstractmethod
    def _register_page_bp(self, bp: APIRouter, page_router: PageRouter):
        """重写此方法,并注册路由
        このメソッドをオーバーライドし、ルーティングを登録してください"""
        ...

    def get_pages(self, db: Session) -> List[PageItem]:
        return self.__get_page_items_from_list(db, self._get_pages(db))

    def __get_page_items_from_list(self, db: Session, ls: list) -> List[PageItem]:
        rt = []
        for i in ls:
            if isinstance(i, PageItem):
                # 当其是一个可返回的元素时
                rt.append(i)
            elif isinstance(i, DeclarativeMeta) and PageTable in i.__mro__:
                # 当其是一个类时,利用db来自动搜索并创建
                data: List[PageTable] = db.query(i).all()
                for d in data:
                    rt.append(PageItem(d.link, d.update_date))
            elif isinstance(i, PageTable):
                # 当其是搜索结果时
                rt.append(PageItem(i.link, i.update_date))
        return rt

    @abstractmethod
    def _get_pages(self, db: Session) -> List[PageItem]:
        """此方法当返回PageItem的列表,暂时被认定为用于创建网站地图
        PageItem 的link为前加/的样式
        """
        ...

    def get_page_bp_set(self):
        return self._page_bp
