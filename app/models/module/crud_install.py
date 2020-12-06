from app.models.user.mdl import User
from . import orm

main_file_path = "app/main.py"
download_path="downloads"

def install_module(module:orm.Module):
    use_module(module)