from abc import abstractmethod, ABCMeta
from typing import List

from fastapi import HTTPException

from app.core.module_class import Module


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
