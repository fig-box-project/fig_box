from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import orm, mod
from app.main import check_token
from app.models.user.mdl import User

bp = APIRouter()

@bp.post('/download')
def download(module_name: str, store_name: str = 'fast-mode',):
    mod.Module(module_name).download(store_name)

@bp.post('/uninstall')
def uninstall(module_name: str):
    mod.Module(module_name).uninstall()

# use----------------------------------------------------------------

@bp.post('/use',description='使用模组')
def use(module:orm.Module):
    module = mod.Module(module.name,"~")
    if module.status == mod.Status.UNUSED:
        module.use()
    else:
        raise HTTPException(status_code=400)
    #     raise HTTPException(status_code=409,detail='已经使用了')
    # else:
    #     raise HTTPException(status_code=404,detail='需要使用的模组不存在')

@bp.post('/unuse',description='禁用模组')
def unuse(module:orm.Module):
    module_bag = mod.get_module_bag(module.name)
    module = module_bag.main_module
    if module.status == mod.Status.USED:
        module.unuse()
    else:
        raise HTTPException(status_code=400)


# store----------------------------------------------------------------

@bp.get('/store/ls')
def view_store(organization_name: str = ""):
    return mod.Store(organization_name).ls()


