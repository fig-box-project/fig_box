from .InputAssetsConnector import InputAssetsConnector
from fastapi import HTTPException
from fastapi.datastructures import UploadFile


class InputUploadConnector(InputAssetsConnector):
    # 允许上传的文件类型
    allow_upload_type = {"jpg", "png", "bmp"}

    def __init__(self, path: str, filename: str, file: UploadFile, limit: int = 5):
        super(InputUploadConnector, self).__init__(path, filename)
        self.__file = file
        self.limit = limit

    # 打包资源到文件
    async def packup(self):
        await super(InputUploadConnector, self).packup()
        self.__check_assert_type()
        self.update_filename()
        asset = await self.__file.read()
        self.check_assert(asset)
        self.save_asset(asset)

    # 检查后缀能否上传
    def __check_assert_type(self):
        if self.filename[self.filename.rfind(".")+1:] not in self.allow_upload_type:
            raise HTTPException(403, "Upload type not allowed")
