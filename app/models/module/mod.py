from enum import Enum
import zipfile
import os

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
    status: Status
    url: str
    description: str
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.status = self.get_status()
    def get_status(self):
        path = 'app/modules.mods'
        para = self.get_params(path,self.name + ' ' + self.version)
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
            crud_install.install_module()
        else:
            pass

    def user(self):
        pass
    def unuse(self):
        pass
    def uninstall(self):
        pass
    # 下载zip
    def download_module(self):
        url = get_module_url(module)
        print(url)
        crud.download_file(url,download_path+'/'+crud.get_module_name(module)+'.zip')
        return True
    

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