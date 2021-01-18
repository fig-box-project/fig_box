import os
import time
from fastapi import UploadFile
from starlette.responses import FileResponse
import zipfile


directory_name = 'files'

# 上传图片
# async def create_file(file:UploadFile,path:str):
#     if check_path_has(path):
#         start = time.time()
#         path = directory_name + path + '/' + file.filename
#         res = await file.read()
#         with open(path, 'wb') as f:
#             f.write(res)
#         return {'time':time.time() - start,'filename':file.filename}
#     else:
#         return None
# 打包下载
def pack_up():
    # 不存在则打包
    if not os.path.exists(directory_name + "templates.zip"):
        zip = zipfile.ZipFile(directory_name+"templates.zip","w",zipfile.ZIP_DEFLATED)
        for path,dirs,files in os.walk(directory_name + "templates"):
            file_path = path.replace(directory_name+"templates","")
            for file in files:
                zip.write(os.path.join(path,file),os.path.join(file_path,file))
        zip.close()
    return FileResponse(directory_name + "templates.zip",media_type='application/zip')

class editor:
    # 删除压缩包
    def del_zip(self,path: str):
        if os.path.exists(directory_name + "templates.zip") and path.split("/")[0]=="templates":
            os.remove(directory_name + "templates.zip")

# 存在则是
def check_path_has(path: str):
    return os.path.exists(directory_name + path)

def check_path_is_dir(path: str):
    return check_path_has(path) and os.path.isdir(directory_name + path)

def write(file_path: str, data: str):
    with open(directory_name + file_path, 'w') as f:
        f.write(data)
    del_zip(file_path)
    return True

def rename(old_file_path: str,new_file_path: str):
    os.rename(old_file_path,new_file_path)
    del_zip(old_file_path)

def create_directory(directory: str):
    if check_path_has("files") == False:
        os.makedirs("files", exist_ok=True)
    os.makedirs(directory_name + directory, exist_ok=True)
    return True

def read(file_path: str):
    with open(directory_name + file_path, 'r') as f:
        return f.read()

def clean(file_path: str = directory_name):
    if file_path[-1:] == "/":
        file_path=file_path[:-1]
    for root, dirs, files in os.walk(file_path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)
    return True

def delete_directory(directory: str):
    try:
        os.rmdir(directory_name + directory)
        return True
    except:
        return False

def delete(file_path: str):
    try:
        os.remove(directory_name + file_path)
        del_zip(file_path)
        return True
    except:
        return False
    

def ls(file_path: str = directory_name):
    if file_path[-1:] == "/":
        file_path=file_path[:-1]
    rt = []
    with os.scandir(file_path) as d:
        for i in d:
            appe = {}
            appe['name'] = i.name
            appe['path'] = (file_path + "/" + i.name)[6:]
            if i.is_dir():
                appe['children'] = ls(file_path + "/" + i.name)
            else:
                appe['file'] = get_type(i.name)
                
            rt.append(appe)
    return rt

def get_type(file_name: str):
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




