import os

directory_name = 'files'

def write(file_path: str, data: str):
    with open(directory_name + file_path, 'w') as f:
        f.write(data)
    return True

def create_directory(directory: str):
    os.makedirs(directory_name + directory, exist_ok=True)
    return True

def read(file_path: str):
    with open(directory_name + file_path, 'r') as f:
        return f.read()

def clean(file_path: str = directory_name):
    for root, dirs, files in os.walk(file_path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)
    return True


def ls(file_path: str = directory_name):
    rt = []
    with os.scandir(file_path) as d:
        for i in d:
            appe = {}
            if i.is_dir():
                appe['name'] = i.name
                appe['children'] = ls(file_path + "/" + i.name)
            else:
                appe['name'] = i.name
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