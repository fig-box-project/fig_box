from fastapi import HTTPException
import os
from enum import Enum, auto
from app.models.settings.crud import settings

class ConflictsMode(Enum):
    # 关于解决冲突的枚举
    AUTO_COUNT_UP = auto()
    AUTO_DEL_IF_EXISTS = auto()

class InputAssetsConnector():
    root_path:str = 'files/assets/'
    mode: ConflictsMode = ConflictsMode.AUTO_COUNT_UP
    limit:int = 0
    size:int = 0

    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    # 用于被重写,被外部调用
    async def packup(self):
        ...

    def update_filename(self):
        # 用于在命名冲突时的处理
        if self.mode is ConflictsMode.AUTO_COUNT_UP:
            self.__auto_count_up()
        elif self.mode is ConflictsMode.AUTO_DEL_IF_EXISTS:
            # 删除文件
            if os.path.exists(self.get_full_path()):
                os.remove(self.get_full_path())
        else:
            raise HTTPException(500,"模式不支持")

    def __auto_count_up(self):
        # 文件名后加_[数字]来解决冲突
        # 分头尾
        i = self.filename.rfind(".")
        filename_head = self.filename[:i]
        filename_foot = self.filename[i:]
        index = 0
        while os.path.exists(self.get_full_path()):
            # 合头尾
            self.filename = f"{filename_head}_{str(index)}{filename_foot}"
            index += 1
    
    def creat_directory_when_not_existing(self):
        os.makedirs(f"{self.root_path}{self.path}", exist_ok=True)

    def check_assert(self, asset):
        # 检查文件大小
        self.size = len(asset)
        if self.limit != 0 and self.size > self.limit * 1000000:
            raise HTTPException(403,"文件的大小超过系统限制")
    
    def save_asset(self, asset):
        # 保存资源
        full_path = self.get_full_path()
        print("保存的位置:" + full_path)
        with open(full_path, 'wb') as f:
            f.write(asset)

    def get_full_path(self):
        return f"{self.root_path}{self.path}/{self.filename}"

    def get_full_url(self):
        return f"{settings.value['domain_port']}/assets/{self.path}/{self.filename}"