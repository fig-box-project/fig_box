from enum import Enum
import zipfile
import os
import shutil
import requests
from app.models.settings.crud import settings

class Status(Enum):
    UNFIND  = 0
    USED    = 1
    UNUSED  = 2

class RunStatus(Enum):
    SUCCESS = 0
    DID     = 1
    FAILURE = 2

class Module:
    name: str
    _status: Status = None
    url: str = ''
    # 不要调用
    tag: str = ''
    description: str
    def __init__(self, name: str):
        self.name = name
    
    # status的get
    @property
    def status(self):
        if self._status == None:
            try:
                status = settings.value["mods"][self.name]["status"]
            except Exception:
                status = None

            if status == "unused":
                self._status = Status.UNUSED
            elif status == "used":
                self._status = Status.USED
            elif status == "unfind":
                self._status = Status.UNFIND
            else:
                raise ValueError
        return self._status
    
    # status的set
    @status.setter
    def status(self, status):
        if self.status == status:
            return
        self._status = status
        if status == Status.UNFIND:
            settings.value["mods"][self.name]["status"] = "unfind"
        elif status == Status.UNUSED:
            settings.value["mods"][self.name]["status"] = "unused"
        elif status == Status.USED:
            settings.value["mods"][self.name]["status"] = "used"
        settings.update()

    # 获取下载地址
    def get_url(self):
        if self.version == '~':
            url = Tool.get_params(store.store_path,'mod ' + self.name)[3]
            # 添加zip文件地址的后缀
            url += '/archive/main.zip'
            return url
        else:
            return None
    
    # 安装
    def install(self):
        if self.status == Status.INCLOUD:
            # 下载
            self.download_module()
            # 解压
            self.unzip()
            #设置状态为未使用
            self.status = Status.UNUSED
            # 使用
            self.use()
        elif self.status == Status.UNFIND:
            return RunStatus.FAILURE
        else:
            return RunStatus.DID

    # 卸载
    def uninstall(self):
        # 禁用
        self.unuse()
        # 删除各种文件
        self.delete_module()
        # 设置状态为云端
        self.status = Status.UNFIND

    # 使用
    def use(self):
        if self.status == Status.UNUSED:
            self.status = Status.USED

    # 禁用
    def unuse(self):
        if self.status == Status.USED:
            name = self.unique_name
            # 更改状态
            self.status = Status.UNUSED
        
    # 解压
    def unzip(self):
        Tool.unzip(self.get_zip_path(),self.get_mod_path(True),self.unique_name)

    # 删除压缩文件和文件夹
    def delete_module(self):
        os.remove(self.get_zip_path())
        shutil.rmtree(self.get_mod_path(False))

    # 下载zip,下载完后将以唯一名称进行保存在downloads中
    def download_module(self):
        Tool.download_file(self.url,self.get_zip_path())

    # 获取压缩包地址
    def get_zip_path(self):
        return 'downloads/'+ self.unique_name +'.zip'

class Store:
    # 商店的文件地址
    store_path = "downloads/store.conf"
    # 商店物品的集合
    _goods = set()
    # 获取商店所有的东西
    def get_goods(self):
        if len(self._goods) > 0:
            return self._goods
        self.check_file()
        list = Tool.get_params_list(self.store_path,'mod ')
        for i in list:
            self._goods.add(i[1])
        return self._goods
            # return [{'name':i[1],'description':''} for i in list]
    
    # 用于api的查看
    def view(self):
        self.check_file()
        list = Tool.get_params_list(self.store_path,'mod ')
        return [{'name':i[1],'status':True,'description':'说明巴拉巴拉'} for i in list]

    # 更新一下商店
    def update(self):
        self.check_file()
        url = Tool.get_params(self.store_path,'path')[1]
        Tool.download_file(url, self.store_path)

    # True为创建了,否则为无创建,在每个api动作前都运行下这个
    def check_file(self):
        if os.path.exists(self.store_path) == False:
            os.mkdir('downloads')
            Tool.download_file('https://raw.githubusercontent.com/fast-mode/store/main/store.conf', self.store_path)
            return True
        else:
            return False

store = Store()

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