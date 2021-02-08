from enum import Enum
import zipfile
import os
import shutil
import requests
import json
from app.models.settings.crud import settings

class RunStatus(Enum):
    SUCCESS = 0
    DID     = 1
    FAILURE = 2

class Module:
    name: str
    status: str
    description: str
    def __init__(self, name: str):
        self.name = name
        try:
            status = settings.value["mods"][self.name]["status"]
        except Exception:
            status = None
            
    def update_status(self):
        try:
            settings.value["mods"][self.name]["status"] = self.status
            settings.update()
        except Exception:
            print("可能模组不存在")
    # 安装
    def download(self, store: str):
        zip_path = 'files/downloads/'+ self.name +'.zip'
        # 下载 TODO:url
        link = f"https://github.com/{store}/{self.name}/archive/main.zip"
        Tool.download_file(link, zip_path)
        # 解压
        Tool.unzip(zip_path,"app/insmodes/",self.name)
        
    # 卸载
    def uninstall(self):
        zip_path = 'files/downloads/'+ self.name +'.zip'
        # 禁用
        self.unuse()
        # 删除各种文件
        os.remove(zip_path)
        shutil.rmtree("app/insmodes/" + self.name)

    # 使用
    def use(self):
        self.status = "used"

    # 禁用
    def unuse(self):
        self.status = "unused"
        
class Store:
    def __init__(self, name: str):
        if name == '':
            name = "fast-mode"
        self.name = name

    # 获取商品列表
    def ls(self):
        url = f"https://api.github.com/orgs/{self.name}/repos"
        j = Tool.get_json(url)
        rt = [x["name"] for x in j]
        return rt

class Tool:
    # 解压zip,重命名
    @staticmethod
    def unzip(oldpath: str, newpath: str,newname: str):
        zipFile = zipfile.ZipFile(oldpath,'r')
        for file in zipFile.namelist():
            zipFile.extract(file,newpath)
        directory_name = zipFile.namelist()[0][:-1]
        zipFile.close()
        # 重命名
        os.rename(newpath + directory_name,newpath + newname)
    
    # 下载文件
    @staticmethod
    def download_file(url:str,path: str):
        print(url)
        res = requests.get(url,stream=True)
        with open(path, 'wb') as dl:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dl.write(chunk)
                # 如果函数存在则给其百分比
    
    # get请求并转换为json
    @staticmethod
    def get_json(url:str):
        rt = requests.get(url).json()
        return rt
        