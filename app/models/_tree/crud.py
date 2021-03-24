from sqlalchemy.orm import Session
from . import orm, conf, mdl
from datetime import datetime
import os
import json

def get_jsondata():
    with open(conf.tree_path,'r') as f:
        json_str = f.read()
    return json.loads(json_str)

class Category:
    _data:dict = {}
    db: Session
    def __init__(self,db: Session):
        self.db = db
        if not os.path.exists("tree.json"):
            with open("tree.json", 'w') as f:
                f.write("{\"id\": 0, \"children\": []}")

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
    
    # def return_fathers(self,id: int):
    #     ids = self.read_database(id)[]

    def read_database(self, id: int):
        return self.db.query(mdl.Category).filter_by(id=id).first()


    def insert(self,father_id: int,leaf:orm.LeafCreate,api_data:orm.CatecoryData):
        data = mdl.Category(**api_data.dict())
        if father_id == 0:
            # 尝试加到数据库
            data.father_ids = '0'
            # 插入到json
            obj = self.data
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
        data.create_date = datetime.now()
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        # 将数据插入到json文件
        new_cate = leaf.getMap()
        new_cate['id'] = data.id
        obj['children'].append(new_cate)
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

    def update(self,leaf:orm.Update):
        if leaf.id == 0:
            return "can no 0"
        # 从数据库中找出该分类
        cate = self.db.query(mdl.Category).filter_by(id=leaf.id).first()
        father_ids = cate.father_ids
        father_id_list = father_ids.split(',')
        # 更新下数据库中的
        cate.name = leaf.name if leaf.name !="" else cate.name
        # self.db.query(mdl.Category).filter_by(id=leaf.id).update({'name':leaf.name})
        # 找出该分类
        obj = self.data
        for i in range(1,len(father_id_list)):
            index = int(father_id_list[i])
            obj = self.search(obj,index)
            if obj is None:
                return None
        for i in range(len(obj['children'])):
            if obj['children'][i]['id'] == leaf.id:
                obj['children'][i] = leaf.get_update_map(obj['children'][i])
                break
        self.data= self.data
        # 更新数据库
        new_data = leaf.dict()
        # 增加一个更新时间戳来更新数据库
        new_data["update_date"] = datetime.now()
        self.db.query(mdl.Category).filter_by(id = leaf.id).update(new_data)
        self.db.commit()

    def search(self,obj,id):
        for o in obj['children']:
            if o['id'] == id:
                return o
    
    # 递归搜索id
    def get_obj(self,id: int,obj=None):
        if obj is None:
            obj = self.data
        for i in range(len(obj['children'])):
            rt = self.get_obj(id,obj['children'][i])
            if rt is not None:
                return rt
            if obj['children'][i]['id'] == id:
                return obj['children'][i]
        return None

        
category :Category = None
def get_category(db: Session):
    global category
    if category is None:
        category = Category(db)
    return category

id_name_map = {}
def id_to_name(db: Session, id: int):
    if id == 0:
        return "root"
    if id not in id_name_map:
        o = get_category(db).get_obj(id)
        if o is not None:
            id_name_map[id] = o['name']
            return o['name']
        else:
            return None
    else:
        return id_name_map[id]
