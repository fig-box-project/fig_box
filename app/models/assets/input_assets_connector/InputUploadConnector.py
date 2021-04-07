from .InputAssetsConnector import InputAssetsConnector
from fastapi.datastructures import UploadFile

class InputUploadConnector(InputAssetsConnector):
    def __init__(self, path: str, filename: str, file: UploadFile, limit: int = 5):
        super(InputUploadConnector, self).__init__(path, filename)
        self.__file = file
        self.limit = limit

    async def packup(self):
        # 打包资源到文件
        self.update_filename()
        asset = await self.__file.read()
        self.check_assert(asset)
        self.save_asset(asset)