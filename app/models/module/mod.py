from enum import Enum
import zipfile
import os
import shutil
import requests
import json
import yaml
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
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/downloads", exist_ok=True)
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

    # 下载
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
        # 搬运yml数据到settings
        settings_path = "app/insmodes/" + self.name + "/settings.yml"
        with open(settings_path, "r") as f:
            mod_settings = yaml.load(f)
        settings.value["mods"][self.name] = mod_settings[self.name]
        settings.value["mods"][self.name]["status"] = "used"
        
        
        # 搬运sitemap到settings
        if "site_maps" in mod_settings:
            if "single_sites" in mod_settings["site_maps"].keys():
                print("-------------")
                settings.value["site_maps"]["single_sites"][self.name] = mod_settings["site_maps"]["single_sites"][self.name]
            if "db_sites" in mod_settings["site_maps"].keys():
                settings.value["site_maps"]["db_sites"][self.name] = mod_settings["site_maps"]["db_sites"][self.name]

        # 更新下设置
        settings.update()

        # 加下log让服务重启
        with open("app/log.py", "a") as f:
            f.write(f"# {self.name} used\n")

    # 禁用
    def unuse(self):
        self.status = "unused"
        # 移除settings的设置
        if self.name in settings.value["mods"]:
            del settings.value["mods"][self.name]
        if self.name in settings.value["site_maps"]["single_sites"]:
            del settings.value["site_maps"]["single_sites"][self.name]
        if self.name in settings.value["site_maps"]["db_sites"]:
            del settings.value["site_maps"]["db_sites"][self.name]

        settings.update()

        # 加log
        with open("app/log.py", "a") as f:
            f.write(f"# {self.name} unused\n")


def local_ls():
    mod_list = os.listdir("app/insmodes")
    mod_list.remove("__init__.py")
    mod_list.remove("__pycache__")
    rt = []
    for i in mod_list:
        if i in settings.value["mods"]:
            rt.append({"name": i, "used":True})
        else:
            rt.append({"name": i, "used":False})
    return rt


# 获取商品列表
def store_ls(name: str):
    url = f"https://api.github.com/orgs/{name}/repos"
    j = Tool.get_json(url)
    insmodes_list = os.listdir("app/insmodes")
    mod_list = [x["name"] for x in j]
    rt = []
    for i in mod_list:
        if i in insmodes_list:
            rt.append({"name": i, "installed":True})
        else:
            rt.append({"name": i, "installed":False})
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
        