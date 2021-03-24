from fastapi import APIRouter, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from app.models import database
from . import orm, crud, mdl
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get('/read/json')
def read_category(db: Session=Depends(database.get_db),):# now_user:User = Depends(check_token),
    return crud.get_category(db).data

@bp.get('/read/database/{id}')
def read_database(id: int,db: Session=Depends(database.get_db)):
    return crud.get_category(db).read_database(id)

@bp.post('/create/{father_id}')
def create_category(father_id: int,leaf:orm.LeafCreate,data:orm.CatecoryData,db: Session=Depends(database.get_db),now_user:User = Depends(check_token),):
    crud.get_category(db).insert(father_id,leaf,data)
    
@bp.delete('/remove/{id}')
def delete_category(id: int,db: Session=Depends(database.get_db),now_user:User = Depends(check_token),):
    crud.get_category(db).remove(id)

@bp.put('/update')
def update_json(leaf:orm.Update,db: Session=Depends(database.get_db),now_user:User = Depends(check_token),):
    crud.get_category(db).update(leaf)
