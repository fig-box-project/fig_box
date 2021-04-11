# 用于打包文件夹为资源
from .InputAssetsConnector import InputAssetsConnector, ConflictsMode
from fastapi import HTTPException
import zipfile
import os

class InputZipDirConnector(InputAssetsConnector):
    def __init__(self, path: str, filename: str, aims: list):
        super(InputZipDirConnector, self).__init__(path, filename)
        if len(aims) == 0:
            raise HTTPException(500,"系统错误,压缩的目标不应为0.")
        self.mode = ConflictsMode.AUTO_DEL_IF_EXISTS
        self.__aims = aims

    async def packup(self):
        await super(InputZipDirConnector, self).packup()
        self.update_filename()
        self.creat_directory_when_not_existing()
        self.__auto_packup()

    def __auto_packup(self):
        # 循环数组并逐次打包入压缩文件
        for i in range(len(self.__aims)):
            self.__auto_zip(self.__aims[i], i)

    def __auto_zip(self, path: str, index: int):
        if os.path.exists(path):
            if os.path.isdir(path):
                self.__zip_dir(path, index)
            else:
                self.__zip_file(path, index)
        else:
            HTTPException(500, f"压缩时找不到文件或文件夹:{path} 索引:{index}")

    def __zip_file(self, path: str, index: int):
        ...

    def __zip_dir(self, directory: str, index: int):
        # 压缩目录
        zip = zipfile.ZipFile(self.get_full_path(),"w",zipfile.ZIP_DEFLATED)
        for path,dirs,files in os.walk(directory):
            # 绝对转相对
            file_path = path.replace(directory,"")[1:]
            print(file_path)
            for file in files:
                # 文件源的路径
                file_from = os.path.join(path,file)
                # 压缩文件内的路径
                file_to = os.path.join("root",str(index),file_path,file)
                zip.write(file_from,file_to)
        zip.close()
        