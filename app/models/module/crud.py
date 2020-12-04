from app.models.user.mdl import User
from . import orm
import fileinput

main_file_path = "app/main.py"

def install_module(module:orm.ModuleInstall):
    cofig_posi = {}
    is_inposi = False
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        if lines[i] == '# for modules>\n':
            cofig_posi['head'] = i
            is_inposi = True
            continue
        elif lines[i] == '# <for modules\n':
            cofig_posi['foot'] = i
            is_inposi = False
            continue
        elif is_inposi:
            lines[i] = '# test str\n'
    with open(main_file_path,'w') as w:
        w.wirte(''.join(lines))
    return cofig_posi

def use_module(module:orm.ModuleUse):
    pass
    
