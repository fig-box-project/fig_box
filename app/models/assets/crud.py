import os
import requests
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from app.models.user.mdl import User
from app.models.settings.crud import settings
from .input_assets_connector.InputUploadConnector import InputUploadConnector
from app.models.assets.input_assets_connector.InputZipDirConnector import InputZipDirConnector


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

    @staticmethod
    async def upload_with_user(asset: UploadFile, filename:str, owner:User, prefix = "", visibility = True, limit = 0):
        connector = InputUploadConnector(f"{prefix}user/{owner.id}",filename,asset, limit)
        await connector.packup()
        link = f"{connector.path}/{connector.filename}"
        return {"url":Assets.path_to_link(link), 
            "link":link, "name":connector.filename, "size":connector.size}

    @staticmethod
    async def migration_packup(parts: list):
        # 替换到实际路径
        path_data = {
            "settings":"settings.yml",
            "templates":"files/templates",
            "photos":"files/assets/photos",
            "database":"db.sqlite"
        }
        for i in range(len(parts)):
            if parts[i] in path_data:
                key = parts[i]
                parts[i] = path_data[key]
                del path_data[key]
            else:
                HTTPException(422,"所输入的内容不符合预设")
        if len(parts) == 0:
            # parts = list(path_data.values())
            parts = ['settings.yml', "db.sqlite"]
        # 开始打包
        connector = InputZipDirConnector("packup","migration.zip",parts)
        await connector.packup()
        return connector.get_full_url()

    @staticmethod
    async def migration_from(old_ip: str):
        url = f"http://{old_ip}/migration/packup"
        responses = requests.get(url).text
        print(responses)
