from fastapi import APIRouter, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from app.models import database
from . import orm, crud, mdl
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get('/read')
def read_category(db: Session=Depends(database.get_db),):# now_user:User = Depends(check_token),
    return crud.get_category(db).data

@bp.post('/create')
def create_category(tree:orm.CategoryCU,db: Session=Depends(database.get_db),): # now_user:User = Depends(check_token),
    crud.get_category(db).insert(tree.id,"test",mdl.Category(name="test"))
    
@bp.delete('/remove/{id}')
def delete_category(id: int,db: Session=Depends(database.get_db),): # now_user:User = Depends(check_token),
    crud.get_category(db).remove(id)

@bp.put('/update/name')
def update_category(tree:orm.CategoryCU,db: Session=Depends(database.get_db),):# now_user:User = Depends(check_token),
    crud.get_category(db).update_name(tree.id,tree.name)