from enum import Enum
import zipfile
import os
import requests

class Status(Enum):
    UNFIND  = 0
    INCLOUD = 1
    USED    = 2
    UNUSED  = 3

class RunStatus(Enum):
    SUCCESS = 0
    DID     = 1
    FAILURE = 2

class ModuleBag:
    name: str
    main_version_status:Status
    def __init__(self, name: str):
        pass


class Module:
    name: str
    version: str
    unique_name: str
    status: Status
    url: str
    description: str
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.unique_name = name + (version if version != '~' else '')
        self.status = self.get_status()
    def get_status(self):
        path = 'app/modules.mods'
        para = Tool.get_params(path,self.name + ' ' + self.version)
        if para == None:
            return Status.INCLOUD
        elif para[2] == 'False':
            return Status.UNUSED
        else:
            return Status.USED
    def get_url(self):
        if self.version == '~':
            url = Tool.get_params('downloads/store.conf','mod ' + self.name)[3]
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
            # 使用
            self.use()
            # 设置状态为已使用
            pass
        elif self.status == Status.UNFIND:
            return RunStatus.FAILURE
        else:
            return RunStatus.DID

    # 卸载
    def uninstall(self):
        # 禁用
        self.unuse()
        # 删除各种文件
        # 设置状态为云端
    def use(self):
        pass
    def unuse(self):
        pass
    def unzip(self):
        Tool.unzip(self.get_zip_path(),self.get_mod_path(True),self.unique_name)

    # 下载zip,下载完后将以唯一名称进行保存在downloads中
    def download_module(self):
        Tool.download_file(self.url,self.get_zip_path())

    # 获取压缩包地址
    def get_zip_path(self):
        return 'downloads/'+ self.unique_name +'.zip'

    # 获取安装后的文件夹位置
    def get_mod_path(self,isFather:bool):
        if isFather:
            return 'app/insmodes/'
        return 'app/insmodes/' + self.unique_name

    

class Tool:
    # 获取文件内的参数
    @staticmethod
    def get_params(path: str,posi: str):
        with open(path,'r') as r:
            lines = r.readlines()
        for line in lines:
            # 历遍所有行,
            if line[:len(posi)] == posi:
                return line.split(' ')
        return None
    
    # 解压zip,重命名
    @staticmethod
    def unzip(oldpath: str, newpath: str,newname: str):
        zipFile = zipfile.ZipFile(oldpath,'r')
        for file in zipFile.namelist():
            zipFile.extract(file,newpath)
        namelist = zipFile.namelist()
        print(namelist)
        zipFile.close()
        # 重命名
        os.rename(newpath+'/'+namelist[0],newpath+'/'+newname)
    
    # 下载文件
    @staticmethod
    def download_file(url:str,path: str,func=None):
        res = requests.get(url,stream=True)
        total_size = int(res.headers.get('content-length'))
        with open(path, 'wb') as dl:
            i = 0
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dl.write(chunk)
                # 如果函数存在则给其百分比
                if func != None:
                    func(i/total_size)
                    i+=1