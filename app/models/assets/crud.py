import os
from fastapi import HTTPException
from app.models.user.mdl import User

class Assets:
    @staticmethod
    def insert(asset, path:str, owner:User, visibility = True, limit = 0):
        # limit为0 时为无限制
        asset_len = len(asset)
        if limit != 0 and asset_len > limit * 1000000:
            raise HTTPException(404,"上传文件的大小超过系统限制")
        # 对于文件已存在时的处理
        if os.path.exists(f"files/assets/{User.id}/{path}"):
            # 分头尾
            i = path.rfind(".")
            path_head = path[:i]
            path_foot = path[i:]
            # 当存在时更改名称再插入
            for j in range(99):
                path = f"{path_head}_{j}{path_foot}"
                if os.path.exists(f"files/assets/{User.id}/{path}"):
                    continue
                with open(f"files/assets/{User.id}/{path}", 'wb') as f:
                    f.write(asset)
                break
        else:
            # 不存在时,直接插入
            with open(f"files/assets/{User.id}/{path}", 'wb') as f:
                f.write(asset)
        return path