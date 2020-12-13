from enum import Enum
from . import crud_install

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