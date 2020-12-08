from app.models.user.mdl import User
from . import orm, crud,crud_use
import requests
import os

download_path = "downloads"
store_path = download_path + "/store.conf"
default_url = 'https://raw.githubusercontent.com/fast-mode/store/main/store.conf'

def update_store():
    if check_file_andadd() == False:
        url = crud.get_params(store_path,'path')[1]
        crud.download_file(url, store_path)

def update_by_default():
    os.mkdir('downloads')
    crud.download_file(default_url, store_path)

def view_store():
    check_file_andadd()
    list = crud.get_params_list(store_path,'mod ')
    return [{'name':i[1],'description':''} for i in list]

def change_url(url:str):
    check_file_andadd()
    crud.set_params(store_path,'path ',['path',url,''])

# True为创建了,否则为无创建,在每个api动作前都运行下这个
def check_file_andadd():
    if os.path.exists(store_path) == False:
        update_by_default()
        return True
    else:
        return False