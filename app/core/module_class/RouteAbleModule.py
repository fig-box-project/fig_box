from abc import ABCMeta, abstractmethod
from typing import Dict

from fastapi import APIRouter

from app.core.module_class import Module
from app.core.module_class.BluePrintSet import BluePrintSet


class RouteAbleModule(Module, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        # 任意なプレフィックスのBluePrintSetのディクショナリ
        self.__free_prefix_map = {}

    def _register_free_prefix(self, prefix: str, unique_key: str) -> APIRouter:
        """呼び出し用、任意なプレフィックス(接頭辞)ルーターを獲得する"""
        if unique_key not in self.__free_prefix_map:
            bps = BluePrintSet(prefix, self._get_tag())
            self.__free_prefix_map[unique_key] = bps
            return bps.get_bp()
        else:
            raise Exception('you can use same key to register routers')

    def get_free_prefix_map(self) -> Dict[str, BluePrintSet]:
        """このメソッドをオーバーライドしないで"""
        return self.__free_prefix_map
