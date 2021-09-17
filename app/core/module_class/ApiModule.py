from abc import ABCMeta, abstractmethod

from fastapi import APIRouter

from app.core.module_class import RouteAbleModule, BluePrintSet


class ApiModule(RouteAbleModule, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self._api_bp = BluePrintSet(
            f'/{self.get_module_name()}', self._get_tag())
        self._register_api_bp(self._api_bp.get_bp())

    @abstractmethod
    def _register_api_bp(self, bp: APIRouter):
        """重写此方法,并注册路由
        このメソッドを実現して @bp.get() などでapiを作成する"""

    def get_api_bp_set(self) -> BluePrintSet:
        return self._api_bp

