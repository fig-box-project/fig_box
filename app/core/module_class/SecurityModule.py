from abc import ABCMeta, abstractmethod


class SecurityModule(Module, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter(self, module: Module) -> List[Callable]:
        ...
