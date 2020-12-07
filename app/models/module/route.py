from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, orm, crud_install
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.post('/install')
def install(module:orm.Module):
    return crud_install.install_module(module)

@bp.post('/use')
def use(module:orm.Module):
    status = crud.get_module_status(module)
    if status == False:
        return crud.use_module(module)
    elif status == True:
        raise HTTPException(status_code=409,detail='已经使用了')
    else:
        raise HTTPException(status_code=404,detail='需要使用的模组不存在')

@bp.post('/unuse')
def unuse(module:orm.Module):
    status = crud.get_module_status(module)
    if status == True:
        return crud.unuse_module(module)
    elif status == False:
        raise HTTPException(status_code=409,detail='已经禁用了')
    else:
        raise HTTPException(status_code=404,detail='需要禁用的模组不存在')

@bp.post('/update-store')
def update_store():
    crud_install.update_store()