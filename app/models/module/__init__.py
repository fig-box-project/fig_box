from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from app.models.mdl.page import PageMdl
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


class AuthItem:
    """始终留意:0是未分配的值(遇到当报错), 1是admin绝对权限, 2是default默认权限"""

    def __init__(self, is_default_auth: bool = False):
        self.is_default_auth = is_default_auth
        self.__auth_key = 0

    def set_auth_key(self, auth_key: int):
        self.__auth_key = auth_key

    def check_auth(self, auth_key: int) -> bool:
        """此处用于检查权限, 可以通过则返回True, 否则返回False"""
        if auth_key == 1:
            return True
        elif auth_key == 1 and self.is_default_auth:
            return True
        elif auth_key == self.__auth_key:
            return True
        elif auth_key == 0:
            raise HTTPException(500, '未注册的权限')
        return False

    def into_auth(self, auth_key: int):
        request = self.check_auth(auth_key)
        if not request:
            raise HTTPException(403, '权限不足')


class AuthModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_auth_items(self) -> List[AuthItem]:
        """在这里返回需要注册的权限"""
        ...

    @abstractmethod
    def auth_register_callback(self):
        """在这里替换掉静态变量"""
        ...


class ApiModule(Module, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
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
        super().__init__()
        self._page_bp = BluePrintSet(f'/{self.get_module_name()}', self._get_tag())
        self.page_router = PageRouter()
        self._register_page_bp(self._page_bp.get_bp(), self.page_router)

    @abstractmethod
    def _register_page_bp(self, bp: APIRouter, page_router: PageRouter):
        """重写此方法,并更改前缀和注册路由"""
        ...

    def get_pages(self, db: Session) -> List[PageItem]:
        return self.__get_page_items_from_list(db, self._get_pages(db))

    def __get_page_items_from_list(self, db: Session, ls: list) -> List[PageItem]:
        rt = []
        for i in ls:
            if isinstance(i, PageItem):
                # 当其是一个可返回的元素时
                rt.append(i)
            elif isinstance(i, DeclarativeMeta) and PageMdl in i.__mro__:
                # 当其是一个类时,利用db来自动搜索并创建
                data: List[PageMdl] = db.query(i).all()
                for d in data:
                    rt.append(PageItem(d.link, d.update_date))
            elif isinstance(i, PageMdl):
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


# 下面是api的实现

class Moudle(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        module_route(bp)

    def _get_tag(self) -> str:
        return '模组'

    def get_module_name(self) -> str:
        return 'moudle'


moudle = Moudle()
