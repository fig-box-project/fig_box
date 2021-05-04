from .OutputAssetsConnector import OutputAssetsConnector
from fastapi import HTTPException
from starlette.responses import FileResponse

typemap = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "png": "image/png",
    "bmp": "image/jpeg",
    "webp": "image/webp",
    "zip": "application/zip",
    "xml": "application/xml"
}


class OutputWebConnector(OutputAssetsConnector):
    def __init__(self, path: str):
        super(OutputWebConnector, self).__init__(path)

    def output(self):
        self.__safty_filter()
        self._check_path()
        media_type = self.__check_name_get_type()
        return FileResponse(self.get_full_path(), media_type=media_type)

    def __safty_filter(self):
        # 安全过滤,如果有两点系统会自动让路径返回上一级,所以要消除..
        # print(self.path)
        if self.path.find("..") != -1:
            raise HTTPException(403, "你不能访问父路径")

    def __check_name_get_type(self):
        type_tips = self.path[self.path.rfind(".") + 1:]
        if type_tips not in typemap:
            raise HTTPException(403, "不支持的数据类型")
        else:
            return typemap[type_tips]
