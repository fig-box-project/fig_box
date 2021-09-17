from abc import ABCMeta, abstractmethod

from fastapi import APIRouter

from app.core.module_class import Module
from app.core.module_class.BluePrintSet import BluePrintSet


class ApiModule(Module, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.__api_bp = BluePrintSet(
            f'/api/v1/{self.get_module_name()}', self._get_tag())
        self._register_api_bp(self.__api_bp.get_bp())

    @abstractmethod
    def _register_api_bp(self, bp: APIRouter):
        """重写此方法,并注册路由
        このメソッドを実現して @bp.get() などでapiを作成する"""
        ...

    def get_api_bp_set(self) -> BluePrintSet:
        return self.__api_bp
