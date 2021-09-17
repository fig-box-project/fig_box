from abc import ABCMeta, abstractmethod

from app.core.module_class import Module


class TableModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_table(self) -> list:
        """重写并返回表名
        テーブルのモデルのリストをリターンしてください、エンジンが自動作成してくれる"""
