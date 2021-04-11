# 用于打包文件夹为资源
from .InputAssetsConnector import InputAssetsConnector, ConflictsMode
import zipfile
import os

class InputZipDirConnector(InputAssetsConnector):
    def __init__(self, path: str, filename: str, directory: str):
        super(InputZipDirConnector, self).__init__(path, filename)
        self.mode = ConflictsMode.AUTO_DEL_IF_EXISTS
        self.__directory = directory

    async def packup(self):
        await super(InputZipDirConnector, self).packup()
        self.update_filename()
        self.creat_directory_when_not_existing()
        self.__zip_dir()

    def __zip_dir(self):
        # 压缩目录
        zip = zipfile.ZipFile(self.get_full_path(),"w",zipfile.ZIP_DEFLATED)
        for path,dirs,files in os.walk(self.__directory):
            file_path = path.replace(self.__directory,"")
            for file in files:
                zip.write(os.path.join(path,file),os.path.join(file_path,file))
        zip.close()
        