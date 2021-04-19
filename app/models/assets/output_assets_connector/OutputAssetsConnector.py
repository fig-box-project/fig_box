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

    def _create_directory(self, path: str, auto_del=False):
        # 为文件创建父文件夹,并返回文件夹路径,autodel为自动删除其下文件
        if os.path.exists(path) and auto_del:
            os.remove(path)
        index = path.rfind("/")
        if index == -1:
            dirs = "."
        else:
            dirs = path[:index]
        print(dirs)
        os.makedirs(dirs, exist_ok=True)
        return dirs
