from fastapi import HTTPException
import os

class InputAssetsConnector():
    root_path:str = 'files/assets/'
    mode = 'auto_count_up'
    limit:int = 0
    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def update_filename(self):
        # 用于在命名冲突时改变文件名
        if self.mode == 'auto_count_up':
            self.__auto_count_up()
        else:
            raise HTTPException(500,"模式不支持")

    # TODO
    def __auto_count_up(self):
        # 文件名后加_[数字]来解决冲突
        # 分头尾
        i = self.filename.rfind(".")
        filename_head = self.filename[:i]
        filename_foot = self.filename[i:]
        index = 0
        while os.path.exists(self.__get_full_path()):
            self.filename = f"{filename_head}_{str(index)}{filename_foot}"
            index += 1
            

        

    def check_assert(self, asset):
        # 检查文件大小
        asset_len = len(asset)
        if self.limit != 0 and asset_len > self.limit * 1000000:
            raise HTTPException(403,"文件的大小超过系统限制")
    
    def save_asset(self, asset):
        # 保存资源
        full_path = self.__get_full_path()
        print("保存的位置:" + full_path)
        with open(full_path, 'wb') as f:
            f.write(asset)

    def __get_full_path(self):
        return f"{self.root_path}{self.path}{self.filename}"