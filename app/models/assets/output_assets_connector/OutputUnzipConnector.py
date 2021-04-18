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
        self.__unzip()

    def __unzip(self):
        with ZipFile(self.get_full_path(), 'r') as f:

            for file in f.infolist():
                print(file.filename)
            # zipFile.extract(file,newpath)
        # directory_name = zipFile.namelist()[0][:-1]
        # zipFile.close()
        # # 重命名
        # os.rename(newpath + directory_name,newpath + newname)
