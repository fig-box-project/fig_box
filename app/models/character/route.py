from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.models.mdl import database
from . import crud
from app.models.user.mdl import User
from . import orm
from ..system.check_token import token

bp = APIRouter()

auth_name = "chara_edit"


@bp.get('/auths/ls', description="查看所有的权限show all authority")
def auths_ls(user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.get_auths()


@bp.get('/myauths', description="显示自己所拥有的权限")
def myauths(user: User = Depends(token.get_token_func())):
    return crud.get_self_auths(user.character)


@bp.get('/charas/ls', description='show all characters')
def charas(user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.get_charas()


@bp.post('/chara/create', description='create a new character')
def create(data: orm.CharaCreate,
           user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.creat_character(data)


@bp.post('/chara/addone', description='增加一个权限到角色')
def addone(data: orm.CharaOne,
           user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.add_one(data)


@bp.post('/chara/removeone', description='删除一个权限从角色')
def removeone(data: orm.CharaOne,
              user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.remove_one(data)


@bp.delete('/chara/{chara_name}', description="delete a character")
def delete(chara_name: str,
           user: User = Depends(token.get_token_func())):
    user.into_auth(auth_name)
    return crud.delete(chara_name)
