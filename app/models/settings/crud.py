from shutil import copyfile
import yaml
import os


class Settings:
    def __init__(self):
        self.yaml_path = "settings.yml"
        if not os.path.exists(self.yaml_path):
            # 复制默认文件
            copyfile("settings_default.yml", "settings.yml")
        # 获取设置
        with open(self.yaml_path, "r") as f:
            self.value: dict = yaml.load(f, Loader=yaml.SafeLoader)

    def update(self):
        with open(self.yaml_path, "w") as f:
            yaml.dump(self.value, f)


class FileDict:
    """构造函数中的路径请不要输入后缀.yml"""

    def __init__(self, path_head: str):
        default_path = f'{path_head}_default.yml'
        cache_path = f'{path_head}.yml'
        self.__path = cache_path
        if not os.path.exists(cache_path):
            # 复制默认文件
            copyfile(default_path, cache_path)
        # 获取设置
        with open(cache_path, "r") as f:
            self.__dict: dict = yaml.load(f, Loader=yaml.SafeLoader)

    def __getitem__(self, index):
        rt = self.__dict[index]
        if isinstance(rt, dict):
            rt._
        return rt

    def __setitem__(self, index, value):
        self.__dict[index] = value

    def update(self):
        with open(self.__path, "w") as f:
            yaml.dump(self.__dict, f)


class ItemDict(dict):
    """此类能够监控对此dict的所有输入行为(测试完成)"""
    def __init__(self, file_dict: FileDict, seq=None, **kwargs):
        self.__file_dict = file_dict
        seq = self.__compare(seq)
        super().__init__(seq, **kwargs)

    def __compare(self, data: dict) -> dict:
        for k in data:
            if isinstance(data[k], dict):
                data[k] = ItemDict(self.__file_dict, data[k])
        return data

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self.__file_dict.update()


# 单例
settings = Settings()
