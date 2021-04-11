# 用于打包文件夹为资源
from .InputAssetsConnector import InputAssetsConnector, ConflictsMode
import requests

class InputDownloadConnector(InputAssetsConnector):
    def __init__(self, path: str, filename: str, url: str):
        super(InputDownloadConnector, self).__init__(path, filename)
        self.mode = ConflictsMode.AUTO_DEL_IF_EXISTS
        self.__url = url

    async def packup(self):
        await super(InputDownloadConnector, self).packup()
        self.update_filename()
        self.creat_directory_when_not_existing()
        self.__download()

    def __download(self):
        res = requests.get(self.__url,stream=True)
        with open(self.get_full_path(), 'wb') as dl:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dl.write(chunk)

        