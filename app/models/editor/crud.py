import os
import time
from fastapi import UploadFile
from starlette.responses import FileResponse
import zipfile
from ..packager.crud import packager

class Editor:
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/templates", exist_ok=True)
    # 检测是否文件夹
    def check_path_is_dir(self,path: str):
        return os.path.exists(path) and os.path.isdir("files/templates/" + path)

    # 写文件
    def write(self,file_path: str, data: str):
        with open("files/templates/{}".format(file_path), 'w') as f:
            f.write(data)
        packager.updated_files("templates")
        return True

    # 重命名
    def rename(self,old_file_path: str,new_file_path: str):
        os.rename(old_file_path,new_file_path)
        packager.updated_files("templates")

    # 读取文件
    def read(self,file_path: str):
        with open("files/templates/{}".format(file_path), 'r') as f:
            return f.read()

    def create_directory(self,path: str):
        os.makedirs("files/templates/{}".format(path),exist_ok=True)

    # 
    def delete_directory(self,directory: str):
        try:
            os.rmdir("files/templates/{}".format(directory))
            packager.updated_files("templates")
            return True
        except:
            return False

    def delete(self,file_path: str):
        try:
            os.remove("files/templates/{}".format(file_path))
            packager.updated_files("templates")
            return True
        except:
            return False
    
    def ls(self,file_path: str = "files/templates/"):
        if file_path[-1:] == "/":
            file_path=file_path[:-1]
        rt = []
        with os.scandir(file_path) as d:
            for i in d:
                appe = {}
                appe['name'] = i.name
                # 权宜之计 TODO
                appe['path'] = ((file_path + "/").replace("templates/","") + i.name)[6:]
                if i.is_dir():
                    appe['children'] = self.ls(file_path + "/" + i.name)
                else:
                    appe['file'] = self.get_type(i.name)
                    
                rt.append(appe)
        return rt

    def get_type(self,file_name: str):
        suffix = os.path.splitext(file_name)[-1][1:]
        if suffix == 'js':
            return 'js'
        elif suffix == 'json':
            return 'json'
        elif suffix == 'png' or suffix == 'ico':
            return 'png'
        elif suffix == 'html':
            return 'html'
        elif suffix == 'md':
            return 'md'
        else:
            return 'txt'

editor = Editor()


