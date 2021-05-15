# 用于打包文件夹为资源
from .InputAssetsConnector import InputAssetsConnector
from fastapi import HTTPException
from zipfile import ZipFile, ZIP_DEFLATED
import os


class InputZipDirConnector(InputAssetsConnector):
    def __init__(self, path: str, filename: str, aims: list, unexist_skip=False):
        """
        # path 是相对assets的路径不需前后斜杠(打包后的路径)
        # aims 是个要打包目标的绝对路径的列表
        """
        super(InputZipDirConnector, self).__init__(path, filename)
        if len(aims) == 0:
            raise HTTPException(500, "系统错误,压缩的目标不应为0.")
        self.mode = InputAssetsConnector.AUTO_DEL_IF_EXISTS
        # 压缩模式默认为索引试压缩
        self.__zip_mode = self.WRAP_WITH_INDEX
        self.unexist_skip = unexist_skip
        self.__aims = aims

    async def packup(self):
        await super(InputZipDirConnector, self).packup()
        self.update_filename()
        self.__auto_packup()

    def __auto_packup(self):
        # 循环数组并逐次打包入压缩文件
        # 只可以r w x a 只读 只写 存在报错写 追加写 默认为r
        # ZIP_DEFLATED 为压缩模式 默认为不压缩
        with ZipFile(self.get_full_path(), "w", ZIP_DEFLATED) as ziper:
            for i in range(len(self.__aims)):
                self.__auto_zip(ziper, self.__aims[i], i)
        print("--------------------------------")

    def __auto_zip(self, ziper: ZipFile, path: str, index: int):
        if os.path.exists(path):
            if os.path.isdir(path):
                self.__zip_dir(ziper, path, index)
            else:
                self.__zip_file(ziper, path, index)
        elif self.unexist_skip:
            ...
        else:
            raise HTTPException(500, f"压缩时找不到文件或文件夹:{path} 索引:{index}")

    def __zip_file(self, ziper: ZipFile, path: str, index: int):
        # file_to = os.path.join("root", str(index), path[path.rfind('/') + 1:])
        file_to = self.__get_aim_path(index, path[path.rfind('/') + 1:])
        # ziper.write(path, file_to)
        self.__write(ziper, path, file_to)

    def __zip_dir(self, ziper: ZipFile, directory: str, index: int):
        # 压缩目录
        for path, dirs, files in os.walk(directory):
            # 绝对转相对
            file_path = path.replace(directory, "")[1:]
            for file in files:
                # 文件源的路径
                file_from = os.path.join(path, file)
                # 压缩文件内的路径
                file_to = self.__get_aim_path(index, os.path.join(path, file))
                # ziper.write(file_from, file_to)
                self.__write(ziper, file_from, file_to)

    WRAP_WITH_INDEX = 0  # 在root文件夹下放置索引以防止文件名冲突
    WRAP_IN_ROOT = 1  # 直接将文件放置在root文件夹下
    WRAP_WITH_PATH = 2  # 系统原来的路径来包装文件

    def set_zip_mode(self, mode: int):
        if mode >= 0 and mode <= 2:
            self.__zip_mode = mode
        else:
            raise HTTPException(500, "zip_mode错误")

    def __write(self, ziper: ZipFile, file_from: str, file_to: str):
        # 写入压缩文件,根据是否利用原系统路径
        if self.__zip_mode == self.WRAP_WITH_PATH:
            ziper.write(file_from)
            print(file_from)
        else:
            ziper.write(file_from, file_to)

    def __get_aim_path(self, index: int, full_path: str):
        if self.__zip_mode == self.WRAP_WITH_INDEX:
            return os.path.join("root", str(index), full_path)
        elif self.__zip_mode == self.WRAP_IN_ROOT:
            return os.path.join("root", full_path)
        else:
            return ""
