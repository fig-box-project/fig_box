from datetime import datetime
from enum import Enum
import zipfile
import os
import shutil
import requests
import yaml
import time
from app.models.settings.crud import settings


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
            settings.value.update()
        except Exception:
            print("可能模组不存在")

    # 下载
    def download(self, store: str):
        zip_path = 'files/downloads/' + self.name + '.zip'
        # 下载 TODO:url
        link = f"https://github.com/{store}/{self.name}/archive/main.zip"
        Tool.download_file(link, zip_path)
        # 解压
        Tool.unzip(zip_path, "app/insmodes/", self.name)
        # 使用
        self.use()

    # 卸载
    def uninstall(self):
        # 禁用
        self.unuse()
        # 删除各种文件
        os.remove('files/downloads/' + self.name + '.zip')
        shutil.rmtree("app/insmodes/" + self.name)

    # 使用
    def use(self):
        self.status = "used"
        if self.name not in settings.value["mods"]:
            settings.value["mods"].insert(0, self.name)  # .append(self.name)
            settings.value.update()
            # 加下log让服务重启
            with open("app/log_tools.py", "a") as f:
                f.write(f"# {str(datetime.now())} {self.name} used\n")

    # 禁用
    def unuse(self):
        self.status = "unused"
        # 移除settings的设置
        if self.name in settings.value["mods"]:
            ls: list = settings.value["mods"]
            ls.remove(self.name)
            settings.value.update()
            # 加log
            with open("app/log_tools.py", "a") as f:
                f.write(f"# {str(datetime.now())} {self.name} unused\n")


def local_ls():
    mod_list = os.listdir("app/insmodes")
    if "__init__.py" in mod_list:
        mod_list.remove("__init__.py")
    if "__pycache__" in mod_list:
        mod_list.remove("__pycache__")
    rt = []
    for i in mod_list:
        if i == ".DS_Store":
            continue
        if i in settings.value["mods"]:
            rt.append({"name": i, "used": True})
        else:
            rt.append({"name": i, "used": False})
    return rt


class Store:
    def __init__(self):
        self.last_time = time.time() - 120
        self.data = {}

    # 获取商品列表
    def store_ls(self, name: str):
        url = f"https://api.github.com/orgs/{name}/repos"
        # 注意,一小时只能调用60次githubapi
        if time.time() - self.last_time > 120:
            self.data[name] = Tool.get_json(url)
            self.last_time = time.time()
        if name in self.data:
            try:
                j = self.data[name]
                insmodes_list = os.listdir("app/insmodes")
                rt = []
                for i in j:
                    i = i["name"]
                    if i in insmodes_list:
                        rt.append({"name": i, "installed": True})
                    else:
                        rt.append({"name": i, "installed": False})
                return rt
            except:
                pass
        return [{"name": "nothing", "installed": False}]


store = Store()


class Tool:
    # 解压zip,重命名
    @staticmethod
    def unzip(oldpath: str, newpath: str, newname: str):
        zipFile = zipfile.ZipFile(oldpath, 'r')
        for file in zipFile.namelist():
            zipFile.extract(file, newpath)
        directory_name = zipFile.namelist()[0][:-1]
        zipFile.close()
        # 重命名
        os.rename(newpath + directory_name, newpath + newname)

    # 下载文件
    @staticmethod
    def download_file(url: str, path: str):
        print(url)
        res = requests.get(url, stream=True)
        with open(path, 'wb') as dl:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dl.write(chunk)
                # 如果函数存在则给其百分比

    # get请求并转换为json
    @staticmethod
    def get_json(url: str):
        rt = requests.get(url).json()
        return rt
