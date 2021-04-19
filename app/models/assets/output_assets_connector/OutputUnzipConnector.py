from .OutputAssetsConnector import OutputAssetsConnector
from zipfile import *


class OutputUnzipConnector(OutputAssetsConnector):
    def __init__(self, path: str, mapping: dict = {}, auto_unzip=False):
        # auto_unzip 是否按照压缩包目录自动解压到指定目录
        self.path = path
        self.__mapping = mapping

    def add_mapping(self, inside_path: str, outside_path: str):
        self.__mapping[inside_path] = outside_path

    def output(self):
        self._check_path()
        self.__unzip()

    def __unzip(self):
        with ZipFile(self.get_full_path(), 'r') as f:
            for file in f.infolist():
                print(file.filename)
                dirs = self._create_directory(file.filename, True)
                f.extract(file, dirs)
        # directory_name = zipFile.namelist()[0][:-1]
        # zipFile.close()
        # # 重命名
        # os.rename(newpath + directory_name,newpath + newname)
