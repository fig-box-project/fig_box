from app.models.user.mdl import User
from . import orm, crud
import requests
import zipfile
import os

main_file_path = "app/main.py"
module_path = "app/insmodes"
download_path="downloads"
store_path = download_path + "/store.conf"
url = "https://github.com/fast-mode/comment/archive/main.zip"
def install_module(module:orm.Module):
    return download_module(module)

def update_store():
    url = crud.get_params(store_path,'path')[1]
    download_file(url, store_path)

# 下载zip
def download_module(module:orm.Module):
    url = get_module_url(module)
    print(url)
    download_file(url,download_path+'/'+crud.get_module_name(module)+'.zip')
    return True

# 解压zip
def unzip(module:orm.Module):
    zipFile = zipfile.ZipFile(download_path+'/'+crud.get_module_name(module)+'.zip','r')
    for file in zipFile.namelist():
        zipFile.extract(file,module_path)
    zipFile.close()
    # 重命名
    os.rename(module_path+'/'+module.name+'-main',module_path+'/'+crud.get_module_name(module))

def get_module_url(module:orm.Module):
    if module.version == '~':
        url = crud.get_params(store_path,'mod ' + module.name)[3]
        # 添加zip文件地址的后缀
        url += '/archive/main.zip'
        return url
    else:
        return None

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
