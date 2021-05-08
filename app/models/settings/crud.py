import types
from shutil import copyfile
import yaml
import os


class Settings:
    def __init__(self):
        self.value = FileDict('settings').getValue()


class FileDict:
    """此类用于解析文件并获得,构造函数中的路径请不要输入后缀.yml"""

    def __init__(self, path_head: str):
        default_path = f'{path_head}_default.yml'
        cache_path = f'{path_head}.yml'
        self.__path = cache_path
        if not os.path.exists(cache_path):
            # 复制默认文件
            copyfile(default_path, cache_path)
        # 获取设置
        with open(cache_path, "r") as f:
            self.__dict: dict = yaml.load(f, Loader=yaml.Loader)

    def getValue(self):
        return ItemDict(self.__dict, self.__path)



#
class ItemDict:
    """此类只能够监控第一层的输入行为(测试完成)"""

    def __init__(self, data: dict, path:str):
        self.__data = data
        self.__path = path

    def __setitem__(self, index, value):
        self.__data[index] = value
        self.update()

    def __getitem__(self, item):
        return self.__data[item]

    def update(self):
        with open(self.__path, "w") as f:
            yaml.dump(self.__data, f)



# 单例
settings = Settings()
