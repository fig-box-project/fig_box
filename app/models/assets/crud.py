import os
from fastapi import HTTPException

class Assets:
    @staticmethod
    def insert(asset, path:str, owner_id, visibility = True, limit = 0):
        # limit为0 时为无限制
        asset_len = len(asset)
        if limit != 0 and asset_len > limit * 1000000:
            raise HTTPException(404,"上传文件的大小超过系统限制")
        while os.path.exists("files/assets/" + path):
            i = path.rfind(".")
            path = path[:i]