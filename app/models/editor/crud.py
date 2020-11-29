import os


directory_name = 'files/'

# 存在则是
def check_path_has(path: str):
    return os.path.exists(directory_name + path)

def check_path_is_dir(path: str):
    return check_path_has(path) and os.path.isdir(directory_name + path)

def write(file_path: str, data: str):
    with open(directory_name + file_path, 'w') as f:
        f.write(data)
    return True

def rename(old_file_path: str,new_file_path: str):
    os.rename(old_file_path,new_file_path)

def create_directory(directory: str):
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

def delete(file_path: str):
    try:
        os.remove(directory_name + file_path)
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



import jinja2
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
templates = Jinja2Templates(directory="files/templates")
# 模版功能
def render_test(request):
    test_path = 'index.html'
    if check_path_has('templates/'+test_path):
        test_data = {'name': '测试名称','request':request}
        return templates.TemplateResponse('index.html',test_data)
    else:
        return 'fail'
