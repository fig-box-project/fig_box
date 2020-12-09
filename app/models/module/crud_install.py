from app.models.user.mdl import User
from . import orm, crud,crud_use,crud_store
import zipfile
import os
import shutil

main_file_path = "app/main.py"
module_path = "app/insmodes"
download_path="downloads"
url = "https://github.com/fast-mode/comment/archive/main.zip"

# 安装模组
def install_module(module:orm.Module):
    download_module(module)
    unzip(module)
    crud_use.use_module(module)

# 重装
def reinstall_module(module:orm.Module):
    crud_use.unuse_module(module)
    delete_directory(module)
    unzip(module)
    crud_use.use_module(module)

# 卸载
def uninstall_module(module:orm.Module):
    crud_use.unuse_module(module)
    delete_module(module)

# 删除zip,模组目录
def delete_module(module:orm.Module):
    os.remove(download_path+'/'+crud.get_module_name(module)+'.zip')
    delete_directory(module)
    
# 删除文件夹
def delete_directory(module:orm.Module):
    shutil.rmtree(module_path+'/'+crud.get_module_name(module))

# 下载zip
def download_module(module:orm.Module):
    url = get_module_url(module)
    print(url)
    crud.download_file(url,download_path+'/'+crud.get_module_name(module)+'.zip')
    return True

# 解压zip,重命名
def unzip(module:orm.Module):
    zipFile = zipfile.ZipFile(download_path+'/'+crud.get_module_name(module)+'.zip','r')
    for file in zipFile.namelist():
        zipFile.extract(file,module_path)
    zipFile.close()
    # 重命名
    os.rename(module_path+'/'+module.name+'-main',module_path+'/'+crud.get_module_name(module))

def get_module_url(module:orm.Module):
    if module.version == '~':
        url = crud.get_params(crud_store.store_path,'mod ' + module.name)[3]
        # 添加zip文件地址的后缀
        url += '/archive/main.zip'
        return url
    else:
        return None

