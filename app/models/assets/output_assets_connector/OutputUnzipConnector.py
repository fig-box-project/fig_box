from .OutputAssetsConnector import OutputAssetsConnector
from zipfile import *


class OutputUnzipConnector(OutputAssetsConnector):
    def __init__(self, path: str, mapping: dict = {}):
        self.path = path
        self.__mapping = mapping

    def add_mapping(self, inside_path: str, outside_path: str):
        self.__mapping[inside_path] = outside_path

    def output(self):
        self._check_path()

    def __unzip(self):
        zipFile = ZipFile(self.path, 'r')
        for file in zipFile.namelist():
            print(file)
            # zipFile.extract(file,newpath)
        # directory_name = zipFile.namelist()[0][:-1]
        # zipFile.close()
        # # 重命名
        # os.rename(newpath + directory_name,newpath + newname)
