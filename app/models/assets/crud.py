import os
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from app.models.user.mdl import User
from app.models.settings.crud import settings
from .input_assets_connector.InputUploadConnector import InputUploadConnector
from .input_assets_connector.InputZipDirConnector import InputZipDirConnector

path_prefix = "files/assets/"
allow_upload_type = {"jpg", "png", "bmp"}

class Assets:
    
    @staticmethod
    def get_link_prefix():
        # 获取链接前缀
        return settings.value["domain_port"] + "/assets"

    @staticmethod
    def path_to_link(path: str):
        return f"{Assets.get_link_prefix()}/{path}"

    # @staticmethod
    # async def packup_dir(path:str):
    #     connector = InputZipDirConnector(f"{path_prefix}packup","test.zip","files/templates")
    #     await connector.packup()

    @staticmethod
    async def insert_with_user(asset: UploadFile, filename:str, owner:User, prefix = "", visibility = True, limit = 0):
        connector = InputUploadConnector(f"{prefix}user/{owner.id}",filename,asset, limit)
        await connector.packup()
        link = f"{connector.path}/{connector.filename}"
        return {"url":Assets.path_to_link(link), 
            "link":link, "name":connector.filename, "size":connector.size}

    @staticmethod
    def insert_with_character():
        ...

