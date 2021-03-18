import os
from fastapi import HTTPException
from app.models.user.mdl import User
from app.models.settings.crud import settings

path_prefix = "files/assets/"
allow_upload_type = {"jpg", "png", "bmp"}

class Assets:
    
    @staticmethod
    def get_link_prefix():
        # 获取链接前缀
        return settings.value["domain_port"] + "/assets"

    @staticmethod
    def insert_file(asset, path: str, filename: str, mode = "auto_countup",limit = 0):
        # 插入
        # 分头尾
        i = filename.rfind(".")
        filename_head = filename[:i]
        filename_foot = filename[i:]
        # 不允许上传的类型要截断
        if filename_foot not in allow_upload_type:
            raise HTTPException(403, "Upload type not allowed")
        if mode == "auto_countup":
            # limit为0 时为无限制
            asset_len = len(asset)
            if limit != 0 and asset_len > limit * 1000000:
                raise HTTPException(404,"上传文件的大小超过系统限制")
            # 对于文件已存在时的处理
            if os.path.exists(f"{path_prefix}{path}/{filename}"):
                # 当存在时更改名称再插入
                for j in range(99):
                    filename = f"{filename_head}_{j}{filename_foot}"
                    if os.path.exists(f"{path_prefix}{path}/{filename}"):
                        continue
                    with open(f"{path_prefix}{path}/{filename}", 'wb') as f:
                        f.write(asset)
                    break
            else:
                # 不存在时,直接插入
                with open(f"{path_prefix}{path}/{filename}", 'wb') as f:
                    f.write(asset)
            return (f"{path_prefix}{path}/{filename}", filename, asset_len)
        else:
            raise HTTPException(500,"模式不支持")

    @staticmethod
    def insert_with_user(asset, filename:str, owner:User, visibility = True, limit = 0):
        rt = Assets.insert_file(asset, f"user/{owner.id}", filename, limit = limit)
        return {"link":f"user/{owner.id}/{rt[1]}", "size":rt[2]}



    @staticmethod
    def insert_with_character():
        ...
