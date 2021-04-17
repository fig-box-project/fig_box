from fastapi import HTTPException
import os


class OutputAssetsConnector():
    def __init__(self,path: str):
        # 这里的path是包括文件名的全路径
        self.path = path

    def _check_path(self):
        if not os.path.exists(self.path):
            raise HTTPException(404,"找不到资源")