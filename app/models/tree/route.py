from fastapi import APIRouter, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from app.models import database
from . import orm, crud
from app.main import check_token
from app.models.user.user import User
bp = APIRouter()

@bp.get('/read')
def read_category():# now_user:User = Depends(check_token),
    return crud.read_all()

@bp.put('/create')
def create_category(tree:orm.CategoryCU,now_user:User = Depends(check_token),):
    if now_user.character.can_edit_tree:
        rt = crud.create(tree)
        if rt:
            return rt
        else:
            raise HTTPException(status_code=404,detail='或许id超过了')
    else:
        raise HTTPException(status_code=403,detail='权限不足')

@bp.put('/delete/{id}')
def delete_category(id: int,now_user:User = Depends(check_token),):
    if now_user.character.can_edit_tree:
        rt = crud.delete(id)
        if rt:
            return rt
        else:
            raise HTTPException(status_code=404,detail='或许id找不到')
    else:
        raise HTTPException(status_code=403,detail='权限不足')

@bp.put('/update')
def update_category(tree:orm.CategoryCU,now_user:User = Depends(check_token),):
    if now_user.character.can_edit_tree:
        rt = crud.update(tree)
        if rt:
            return rt
        else:
            raise HTTPException(status_code=404,detail='或许id找不到')
    else:
        raise HTTPException(status_code=403,detail='权限不足')