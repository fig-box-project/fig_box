from fastapi import APIRouter, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from app.models import database
from . import crud
from app.main import check_token
from app.models.user.mdl import User
from . import orm
bp = APIRouter()

@bp.get('/auths/ls', description="查看所有的权限")
def auths_ls():
    return crud.get_auths()
    
@bp.get('/charas/ls', description = '')
def charas():
    return crud.get_charas()

@bp.post('/chara/create', description = '')
def create(data: orm.CharaCreate):
    return crud.creat_character(data)
	
@bp.delete('/chara/{chara_name}')
def delete(chara_name:str):
    return crud.delete(chara_name)
	