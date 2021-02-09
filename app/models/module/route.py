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
def unuse(module_name: str):
    module = mod.Module(module_name)
    module.unuse()


# store----------------------------------------------------------------

@bp.get('/store/ls')
def view_store(organization_name: str = ""):
    return mod.Store(organization_name).ls()


