from app.models.user.mdl import User
from . import orm
import fileinput

main_file_path = "app/main.py"

def install_module(module:orm.Module):
    use_module(module)

def unuse_module(module:orm.Module):
    delete_code_main(module)
    moduleStatus = orm.ModuleStatus(**module.dict(),status=False)
    set_module(moduleStatus)
    return true

# 使用模组--------------------------------
def use_module(module:orm.Module):
    insert_code_main(module)
    # 更改状态并保存
    moduleStatus = orm.ModuleStatus(**module.dict(),status=True)
    set_module(moduleStatus)
    return True

def get_module_status(module:orm.Module):
    sta_module = check_module(module)
    if sta_module == None:
        return None
    return check_module(module).status

# 获取模组的tag
def get_module_tag(module:orm.Module):
    path = 'app/models/' + get_module_name(module) + '/config.conf'
    return get_params(path,'api_tag')[1]

# 获取模组的唯一名字,当为master时不变,当有版本时将_+版本号
def get_module_name(module:orm.Module):
    if module.version == '~':
        return module.name
    else:
        version = module.version.split('.')[2]
        return module.name + '_' + version

# 插入代码到main文件
def insert_code_main(module:orm.Module):
    name = get_module_name(module)
    tag = get_module_tag(module)
    code = \
f'''# {name}>
from .models.module.route import bp as {name}_route
app.include_router(
    {name}_route,
    prefix=url_prefix + '/{name}',
    tags=['{tag}'],)
# <{name}
'''
    insert_str_main(code)

# 从main删除代码--------------------------------
def delete_code_main(module:orm.Module):
    name = get_module_name(module)
    del_module_area_main(name)

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
    del lines[head:foot]
    with open(main_file_path,'w') as w:
        w.write(''.join(lines))

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


# 可用于获取模组状态
def check_module(module:orm.Module):
    # 打开标识所有模组的文件
    path = 'app/modules.mods'
    li = get_params(path,module.name + ' ' + module.version)
    if li[1] == module.version:
        return orm.ModuleStatus(**module.dict(),status = li[2]=='True')
    return None

def set_module(module:orm.ModuleStatus):
    line_data = [module.name,module.version,str(module.status) + ' ']
    path = 'app/modules.mods'
    set_params(path,module.name+' '+module.version,line_data)

# 获取文件内的参数
def get_params(path: str,posi: str):
    with open(path,'r') as r:
        lines = r.readlines()
    for line in lines:
        # 历遍所有行,
        if line[:len(posi)] == posi:
            return line.split(' ')
    return None

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