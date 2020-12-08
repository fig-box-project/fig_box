from app.models.user.mdl import User
from . import orm
import requests

main_file_path = "app/main.py"

# 获取模组的唯一名字,当为master时不变,当有版本时将_+版本号
def get_module_name(module:orm.Module):
    if module.version == '~':
        return module.name
    else:
        version = module.version.split('.')[2]
        return module.name + '_' + version

# 获取文件内的参数
def get_params(path: str,posi: str):
    with open(path,'r') as r:
        lines = r.readlines()
    for line in lines:
        # 历遍所有行,
        if line[:len(posi)] == posi:
            return line.split(' ')
    return None

# 获取所有列表的参数
def get_params_list(path: str,posi: str):
    rt = []
    with open(path,'r') as r:
        lines = r.readlines()
    for line in lines:
        # 历遍所有行,
        if line[:len(posi)] == posi:
            rt.append(line.split(' '))
    return rt

# 设置文件内的参数
def set_params(path: str,posi:str,line_data:list):
    line_str = ' '.join(line_data) + '\n'
    with open(path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        # 历遍所有行,
        if lines[i][:len(posi)] == posi:
            lines[i] = line_str
            break
    with open(path,'w') as w:
        w.write(''.join(lines))

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
