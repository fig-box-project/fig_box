from typing import Optional


class Package:
    def __init__(self, name: str, imp_str: Optional[str] = None):
        """"""
        self.name = name
        if imp_str is not None:
            self.import_str = imp_str
        else:
            self.import_str = name
