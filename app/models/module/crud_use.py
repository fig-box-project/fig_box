from app.models.user.mdl import User
from . import orm, crud

main_file_path = "app/main.py"

def unuse_module(module:orm.Module):
    if get_module_status(module) == True:
        delete_code_main(module)
        moduleStatus = orm.ModuleStatus(**module.dict(),status=False)
        set_module(moduleStatus)
        return True
    else:
        return False

# 使用模组--------------------------------
def use_module(module:orm.Module):
    if get_module_status(module) == False:
        insert_code_main(module)
        # 更改状态并保存
        moduleStatus = orm.ModuleStatus(**module.dict(),status=True)
        set_module(moduleStatus)
        return True
    else:
        return False

def get_module_status(module:orm.Module):
    sta_module = check_module(module)
    if sta_module == None:
        return None
    return check_module(module).status

# 获取模组的tag
def get_module_tag(module:orm.Module):
    path = 'app/insmodes/' + crud.get_module_name(module) + '/config.conf'
    return crud.get_params(path,'api_tag')[1]

# 从main删除代码--------------------------------
def delete_code_main(module:orm.Module):
    name = crud.get_module_name(module)
    del_module_area_main(name)

# 插入代码到main文件
def insert_code_main(module:orm.Module):
    name = crud.get_module_name(module)
    tag = get_module_tag(module)
    code = \
f'''# {name}>
from .insmodes.{name}.route import bp as {name}_route
app.include_router(
    {name}_route,
    prefix=url_prefix + '/{name}',
    tags=['{tag}'],)
# <{name}
'''
    insert_str_main(code)

# 插入文字到main文件
def insert_str_main(s: str):
    is_inposi = False
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        if lines[i] == '# for modules>\n':
            is_inposi = True
            continue
        elif is_inposi:
            lines[i] = '\n' + s
            break
    with open(main_file_path,'w') as w:
        w.write(''.join(lines))

# 备用方法,用来获取模组在main的代码区间
def get_posi_main():
    cofig_posi = {}
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        if lines[i] == '# for modules>\n':
            cofig_posi['head'] = i
            continue
        elif lines[i] == '# <for modules\n':
            cofig_posi['foot'] = i
            break
    return cofig_posi

# 删除模组所在的区间
def del_module_area_main(name:str):
    with open(main_file_path,'r') as r:
        lines = r.readlines()
    for i in range(len(lines)):
        if lines[i] == f'# {name}>\n':
            head = i
            continue
        elif lines[i] == f'# <{name}\n':
            foot = i
            break
    del lines[head:foot+1]
    with open(main_file_path,'w') as w:
        w.write(''.join(lines))

# 可用于获取模组状态
def check_module(module:orm.Module):
    # 打开标识所有模组的文件
    path = 'app/modules.mods'
    li = crud.get_params(path,module.name + ' ' + module.version)
    if li[1] == module.version:
        return orm.ModuleStatus(**module.dict(),status = li[2]=='True')
    return None

def set_module(module:orm.ModuleStatus):
    line_data = [module.name,module.version,str(module.status) + ' ']
    path = 'app/modules.mods'
    crud.set_params(path,module.name+' '+module.version,line_data)
