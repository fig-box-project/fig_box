from fastapi import APIRouter


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