from app.models.user.mdl import User
from . import orm
import fileinput

main_file_path = "app/main.py"

def install_module(module:orm.ModuleInstall):
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in lines:
        if i == '# for modules>\n':
            return True
    for i in range(114):
        if i == 105:
            return lines[i]
    return {'count':len(lines),} 