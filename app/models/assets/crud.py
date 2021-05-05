import requests
from fastapi import HTTPException
from fastapi.datastructures import UploadFile
from app.models.user.mdl import User
from app.models.settings.crud import settings
from .input_assets_connector import *

path_prefix = "files/assets/"
allow_upload_type = {"jpg", "png", "bmp"}


class Assets:

    @staticmethod
    def get_link_prefix(host: str = None):
        """获取链接前缀"""
        if host is not None:
            return host + '/assets'
        return settings.value["domain_port"] + "/assets"

    @staticmethod
    def path_to_link(path: str, host: str = None):
        """通过路径获取完整url"""
        print(host)
        return f"{Assets.get_link_prefix(host)}/{path}"

    @staticmethod
    async def upload_with_user(asset: UploadFile, filename: str, owner: User, prefix="", visibility=True, limit=0):
        connector = InputUploadConnector(
            f"{prefix}user/{owner.id}", filename, asset, limit)
        await connector.packup()
        link = f"{connector.path}/{connector.filename}"
        return {"url": Assets.path_to_link(link),
                "link": link, "name": connector.filename, "size": connector.size}

    @staticmethod
    async def migration_packup(parts: list):
        # 替换到实际路径
        path_data = {
            "settings": "settings.yml",
            "templates": "files/templates",
            "photos": "files/assets/photos",
            "database": "db.sqlite"
        }
        for i in range(len(parts)):
            if parts[i] in path_data:
                key = parts[i]
                parts[i] = path_data[key]
                del path_data[key]
            else:
                HTTPException(422, "所输入的内容不符合预设")
        if len(parts) == 0:
            parts = list(path_data.values())
            # parts = ['settings.yml', "db.sqlite"]
        # 开始打包
        connector = InputZipDirConnector(
            "packup", "migration.zip", parts, unexist_skip=True)
        connector.__zip_mode = InputZipDirConnector.WRAP_IN_ROOT
        await connector.packup()
        return f"{connector.path}/{connector.filename}"

    @staticmethod
    async def migration_from(old_ip: str):
        url = f"{old_ip}/migration/packup"
        responses = requests.get(url).text
        # 去除引号,成功返回路径
        link = f"{old_ip}/assets/{responses[1:-1]}"
        print(link)
        connector = InputDownloadConnector("dl", "sss.zip", link)
        await connector.packup()
