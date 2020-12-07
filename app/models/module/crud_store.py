from app.models.user.mdl import User
from . import orm, crud,crud_use
import requests

store_path = download_path + "/store.conf"

def update_store():
    url = crud.get_params(store_path,'path')[1]
    download_file(url, store_path)