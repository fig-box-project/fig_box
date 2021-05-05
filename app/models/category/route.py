from typing import List

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from app.models.category import orm, mdl
from app.models.mdl import database
from app.models.system import token
from app.models.user.mdl import User

bp = APIRouter()


class CategoryServer:
    def __init__(self, db: Session, service: str):
        all_services = db.query(mdl.Category).filter_by(title=service).all()
        if len(all_services) == 0:
            raise HTTPException(412, '没有找到此服务,你是否已创建此服务?')
        self.__service: mdl.Category = all_services[0]
        self.__db = db

    def ls(self):
        return [{
            'id': self.__service.id,
            'title': self.__service.title,
            'description': self.__service.description,
            'children': self.__get_children(self.__service)
        }]

    def get_id(self):
        return self.__service.id

    def __get_children(self, category: mdl.Category):
        children: List[mdl.Category] = self.__db.query(mdl.Category).filter_by(father_id=category.id).all()

        rt = []
        for i in children:
            rt.append({
                'id': i.id,
                'title': i.title,
                'description': i.description,
                'children': self.__get_children(i)
            })
        return rt


@bp.post('/create/service')
def create_categor(data: orm.CategoryCU, db: Session = Depends(database.get_db),
                   now_user: User = Depends(token.check_token), ):
    # 查找有无相同的服务
    if data.title in ls_service(db):
        raise HTTPException(403, '已存在同名服务')
    # 插入
    data.father_id = 0
    data = mdl.Category(**data.dict())
    db.add(data)
    db.commit()
    return {'service': data.title}


@bp.get('/ls/service')
def ls_service(db: Session = Depends(database.get_db)) -> set:
    all_services = db.query(mdl.Category).filter_by(father_id=0).all()
    rt = set()
    for i in all_services:
        rt.add(i.title)
    return rt


# ---服务内处理---


@bp.get('/{service}/ls')
def ls(service: str, db: Session = Depends(database.get_db)):
    return CategoryServer(db, service).ls()


@bp.post('/{service}/create')
def create_category(service: str, data: orm.CategoryCU, db: Session = Depends(database.get_db),
                    now_user: User = Depends(token.check_token), ):
    server = CategoryServer(db, service)
    if data.father_id == 0:
        data.father_id = server.get_id()
    data = mdl.Category(**data.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {'id': data.id}


@bp.delete('/{service}/delete')
def delete_category(id: int, db: Session = Depends(database.get_db), now_user: User = Depends(token.check_token), ):
    db.query(mdl.Category).filter_by(id=id).delete()
    db.commit()


@bp.put('/{service}/update')
def update_json(service: str, id: int, data: orm.CategoryCU, db: Session = Depends(database.get_db),
                now_user: User = Depends(token.check_token), ):
    server = CategoryServer(db, service)
    if data.father_id == 0:
        data.father_id = server.get_id()
    insert_data = data.dict()
    db.query(mdl.Category).filter_by(id=id).update(insert_data)
    db.commit()

# @bp.get('/{service}/cd')
# def cd(id: int, db: Session = Depends(database.get_db)):
#     return Tools.get_children(id, db)
