from fastapi import HTTPException
import os


class OutputAssetsConnector():
    root_path = 'files/assets'

    def __init__(self, path: str):
        # 这里的path是包括文件名的全路径
        self.path = path

    def _check_path(self):
        if not os.path.exists(self.get_full_path()):
            raise HTTPException(404, "找不到资源")

    def get_full_path(self):
        return f"{self.root_path}/{self.path}"
