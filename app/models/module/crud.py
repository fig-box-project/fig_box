from app.models.user.mdl import User
from . import orm
import fileinput

main_file_path = "app/main.py"

def install_module(module:orm.ModuleInstall):
    cofig_posi = {}
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        if lines[i] == '# for modules>\n':
            cofig_posi['head'] = i
        elif lines[i] == '# <for modules\n':
            cofig_posi['foot'] = i
    return cofig_posi

def use_module(module:orm.ModuleUse):
    pass
    
