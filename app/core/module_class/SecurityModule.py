from abc import ABCMeta, abstractmethod
from typing import List, Callable

from app.core.module_class import Module


class SecurityModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter(self, module: Module) -> List[Callable]:
        ...
