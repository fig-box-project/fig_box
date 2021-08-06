from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Set

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from app.models.mdl import PageMdl
from app.models.mdl.database import Base
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
    """传入一个模组里唯一的权限标识字符串,用于角色中的权限搜索"""

    def __init__(self, auth_name: str, is_default_auth: bool = False):
        self.is_default_auth = is_default_auth
        self.auth_name = auth_name
        self.name = ''

    def set_mod_name(self, mod_name):
        self.name = f'<{mod_name}>{self.auth_name}'

    def check_auth(self, auth_list: list) -> bool:
        """此处用于检查权限, 可以通过则返回True, 否则返回False"""
        if self.is_default_auth and 'default' in auth_list:
            return True
        elif self in auth_list:
            return True
        elif 'admin' in auth_list:
            return True
        else:
            return False

    def into_auth(self, auth_list: list):
        request = self.check_auth(auth_list)
        if not request:
            raise HTTPException(403, '你的权限不足')


class AuthModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_auth_items(self) -> List[AuthItem]:
        """在这里返回需要注册的权限"""
        ...


class TableModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_table(self) -> list:
        """重写并返回表名"""


class ApiModule(Module, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._api_bp = BluePrintSet(
            f'/api/v1/{self.get_module_name()}', self._get_tag())
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
        self._page_bp = BluePrintSet(
            f'/{self.get_module_name()}', self._get_tag())
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
        return 'モジュール管理'

    def get_module_name(self) -> str:
        return 'moudle'


moudle = Moudle()
