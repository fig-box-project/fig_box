from abc import ABCMeta, abstractmethod


class Module(metaclass=ABCMeta):
    @abstractmethod
    def _get_tag(self) -> str:
        """swaggerに表示するtagをリターンしてください"""
        ...

    @abstractmethod
    def get_module_name(self) -> str:
        """このメソッドを実現してモジュールの名前をリターンしてください"""
        ...

    def is_need_ip_filter(self):
        return False
