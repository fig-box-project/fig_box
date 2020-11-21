from sqlalchemy.orm import Session
from . import orm, conf
import json

def read_all():
    with open(conf.tree_path,'r') as f:
        return f.read()

# 反回non表示创建失败
def create(tree:orm.CategoryCU):
    with open(conf.tree_path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    # create tree
    is_created = __create_tree(tree_map, tree.id,tree.name,tree_map['max']+1)
    tree_map['max']+=1
    # write it
    with open(conf.tree_path,'w') as f:
        f.write(json.dumps(tree_map))
    if is_created:
        return tree_map
    else:
        return None
# |||||||||||||||||||||||||||||||||||||||||||||||||
def __create_tree(tree_map:dict,id,insert_name,insert_id):
    for k in tree_map.keys():
        if k == 'id' and tree_map[k] == id:
            tree_map[insert_name] = {
                "id":insert_id,
                "name":insert_name
            }
            return tree_map
        if k != 'id' and k != 'name' and k != 'max':
            has = __create_tree(tree_map[k],id,insert_name,insert_id)
            if has != None:
                tree_map[k] = has
    return None

def delete(id: int):
    with open(conf.tree_path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    suc =  del_tree(tree_map,id)
    if suc != None:
        with open(conf.tree_path,'w') as f:
            f.write(json.dumps(tree_map))
        return tree_map
    else:
        return None

def del_tree(tree_map:dict,id):
    if id != 0:
        for k in tree_map.keys():
            # if k == 'id' and tree_map[k] == id:
            #     return tree_map['name']
            if k != 'id' and k != 'name' and k != 'max':
                son_id = tree_map[k]['id']
                if son_id == id:
                    tree_map.pop(k)
                    return tree_map
                has = del_tree(tree_map[k],id)
                if has != None:
                    tree_map[k] = has
                    return tree_map
    return None

# 怀疑有错误
def update(tree: orm.CategoryCU):
    with open(conf.tree_path,'r') as f:
        json_str = f.read()
    tree_map = json.loads(json_str)
    suc =  update_tree(tree_map,tree.id,tree.name)
    if suc != None:
        with open(conf.tree_path,'w') as f:
            f.write(json.dumps(tree_map))
        return tree_map
    else:
        return None

def update_tree(tree_map:dict,id,name):
    if id != 0:
        for k in tree_map.keys():
            # if k == 'id' and tree_map[k] == id:
            #     return tree_map['name']
            if k != 'id' and k != 'name' and k != 'max':
                son_id = tree_map[k]['id']
                if son_id == id:
                    tree_map[name] = tree_map.pop(k)
                    tree_map[name]['name'] = name
                    return tree_map
                has = update_tree(tree_map[k],id,name)
                if has != None:
                    tree_map[k] = has
                    return tree_map
    return None