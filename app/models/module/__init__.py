from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from fastapi import APIRouter
from requests import Session

from app.models.module.route import module_route
from app.models.page.crud import PageRouter


class BluePrintSet:
    def __init__(self, prefix: str, tag='null'):
        self.__bp = APIRouter()
        self.__tag = tag
        self.__prefix = prefix

    def get_bp(self):
        return self.__bp

    def set_tag(self, tag: str):
        self.__tag = tag

    def get_tags(self):
        return [self.__tag]

    def append_prefix(self, prefix: str):
        """追加文本到前缀,注意格式为/sample/something"""
        self.__prefix += prefix

    def change_prefix(self, prefix: str):
        """更改整个前缀,注意格式为/sample/something"""
        self.__prefix = prefix

    def get_prefix(self):
        return self.__prefix


class Module(metaclass=ABCMeta):
    @abstractmethod
    def _get_tag(self) -> str:
        ...

    @abstractmethod
    def get_module_name(self) -> str:
        ...

    def is_need_ip_filter(self):
        return False


class ApiModule(Module, metaclass=ABCMeta):

    def __init__(self):
        self._api_bp = BluePrintSet(f'/api/v1/{self.get_module_name()}', self._get_tag())
        self._register_api_bp(self._api_bp.get_bp())

    @abstractmethod
    def _register_api_bp(self, bp: APIRouter):
        """重写此方法,并更改前缀和注册路由self._api_bp可以改前缀"""
        ...

    def get_api_bp_set(self) -> BluePrintSet:
        return self._api_bp


class PageItem:
    """暂时用于sitemap,如有其它用处时可扩张"""

    def __init__(self, link: str, update_date: datetime):
        self.link = link
        self.update_date = update_date


class PageModule(Module, metaclass=ABCMeta):
    def __init__(self):
        print('afsdf')
        self._page_bp = BluePrintSet(f'/{self.get_module_name()}', self._get_tag())
        self.page_router = PageRouter()
        self._register_page_bp(self._page_bp.get_bp(), self.page_router)

    @abstractmethod
    def _register_page_bp(self, bp: APIRouter, page_router: PageRouter):
        """重写此方法,并更改前缀和注册路由"""
        ...

    @abstractmethod
    def get_pages(self, db: Session) -> List[PageItem]:
        """此方法当返回PageItem的列表,暂时被认定为用于创建网站地图
        PageItem 的link为前加/的样式
        """
        ...

    def get_page_bp_set(self):
        return self._page_bp


class Moudle(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        module_route(bp)

    def _get_tag(self) -> str:
        return '模组'

    def get_module_name(self) -> str:
        return 'moudle'

moudle = Moudle()