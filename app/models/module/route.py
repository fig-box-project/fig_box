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
def use(module_name: str):
    module = mod.Module(module_name)
    module.use()

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


