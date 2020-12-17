from sqlalchemy.orm import Session
from . import orm, conf, mdl
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

class Leaf:
    id: int = 0
    name: str = ""
    children: list = []
    description: str = ""
    def getMap(self):
        return self.__dict__
    def get_update_map(self,old_data:dict):
        if self.name != "":
            old_data["name"] = self.name
        if self.description != "":
            old_data["description"] = self.description
        return old_data

class Category:
    _data:dict = {}
    db: Session
    def __init__(self,db: Session):
        self.db = db

    # get data
    @property
    def data(self):
        if len(self._data) == 0:
            with open(conf.tree_path,'r') as f:
                json_str = f.read()
            self._data = json.loads(json_str)
        return self._data
    
    # set data
    @data.setter
    def data(self, data):
        with open(conf.tree_path,'w') as f:
            f.write(json.dumps(data))
        self._data = data

    def insert(self,father_id: int,leaf:Leaf,data:mdl.Category):
        if father_id == 0:
            # 尝试加到数据库
            data.father_ids = '0'
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            leaf.id = data.id
            # 插入到json
            new_cate = leaf.getMap()
            self.data['children'].append(new_cate)
            # 上面没调用seter,所以
            self.data = self.data
        else:
            # 从数据获取祖先的id们
            father_ids = self.db.query(mdl.Category).filter(mdl.Category.id==father_id).first().father_ids
            father_id_list = father_ids.split(',')
            # 找出对应的父obj以作准备,如果找不到就立即跳出程序
            obj = self.data
            for i in range(1,len(father_id_list)):
                index = int(father_id_list[i])
                obj = self.search(obj,index)
                if obj is None:return None
            obj = self.search(obj,father_id)
            if obj is None:return None
            # 插入数据库并获取新id
            data.father_ids= father_ids + "," + str(father_id)
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
            leaf.id = data.id
            # 将数据插入到json文件
            obj['children'].append(leaf.getMap())
            self.data = self.data

    def remove(self,id: int):
        # 从数据库中找出该分类
        cate = self.db.query(mdl.Category).filter_by(id=id).first()
        father_ids = cate.father_ids
        father_id_list = father_ids.split(',')
        # 从数据库删除
        self.db.delete(cate)
        self.db.commit()
        # 从json删除
        obj = self.data
        for i in range(1,len(father_id_list)):
            index = int(father_id_list[i])
            obj = self.search(obj,index)
            if obj is None:return None
        for i in range(len(obj['children'])):
            if obj['children'][i]['id'] == id:
                obj['children'].pop(i)
        self.data= self.data

    def update_json(self,leaf:Leaf):
        # 从数据库中找出该分类
        cate = self.db.query(mdl.Category).filter_by(id=id).first()
        father_ids = cate.father_ids
        father_id_list = father_ids.split(',')
        # 更新下数据库中的
        cate.name = leaf.name if leaf.name !="" else cate.name
        self.db.commit()
        # 找出该分类
        obj = self.data
        for i in range(1,len(father_id_list)):
            index = int(father_id_list[i])
            obj = self.search(obj,index)
            if obj is None:return None
        for i in range(len(obj['children'])):
            if obj['children'][i]['id'] == id:
                obj['children'][i] = leaf.get_update_map(obj['children'][i])
                break
        self.data= self.data
    def update_database()
    def search(self,obj,id):
        for o in obj['children']:
            if o['id'] == id:
                return o
        
category :Category = None
def get_category(db: Session):
    global category
    if category is None:
        category = Category(db)
    return category


