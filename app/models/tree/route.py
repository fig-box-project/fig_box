from fastapi import APIRouter, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from app.models import database
from . import orm, crud, mdl
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get('/read')
def read_category():# now_user:User = Depends(check_token),
    return crud.read_all()

@bp.post('/create')
def create_category(tree:orm.CategoryCU,db: Session=Depends(database.get_db),): # now_user:User = Depends(check_token),
    crud.get_category(db).insert(tree.id,"test",mdl.Category(name="test"))
    

@bp.delete('/remove/{id}')
def delete_category(id: int,db: Session=Depends(database.get_db),): # now_user:User = Depends(check_token),
    crud.get_category(db).remove(id)

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