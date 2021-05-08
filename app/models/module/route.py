from fastapi import APIRouter
from . import mod

bp = APIRouter()


@bp.post('/download')
def download(module_name: str, store_name: str = 'fast-mode',):
    mod.Module(module_name).download(store_name)


@bp.post('/uninstall')
def uninstall(module_name: str):
    mod.Module(module_name).uninstall()

# use----------------------------------------------------------------


@bp.post('/use', description='使用模组')
def use(module_name: str):
    module = mod.Module(module_name)
    module.use()


@bp.post('/unuse', description='禁用模组')
def unuse(module_name: str):
    module = mod.Module(module_name)
    module.unuse()


@bp.get('/ls', description='查看本地模组情况(未实现,返回个数组)')
def ls():
    return mod.local_ls()


# store----------------------------------------------------------------

@bp.get('/store/ls')
def view_store(organization_name: str = "fast-mode"):
    return mod.store.store_ls(organization_name)
