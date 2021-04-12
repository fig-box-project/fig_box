from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from app.models.settings.crud import settings
import os
from .crud import Assets

assets_path_prefix = settings.value["assets_path"]
os.makedirs(assets_path_prefix, exist_ok=True)

bp = APIRouter()

typemap = {
    "jpg":"image/jpeg",
    "jpeg":"image/jpeg",
    "gif":"image/gif",
    "png":"image/png",
    "bmp":"image/jpeg",
    "webp":"image/webp",
    "zip":"application/zip",
    "xml":"application/xml"
}

@bp.get("/assets/{assets_path:path}", description = "获取资源链接")
def get_assets(assets_path: str):
    # 安全过滤,如果有两点系统会自动让路径返回上一级,所以要消除..
    assets_path = assets_path.replace("..","")
    # 文件的路径
    path = assets_path_prefix + "/" + assets_path
    type_tips = path[path.rfind(".") + 1:]

    if os.path.exists(path):
        if type_tips in typemap:
            return FileResponse(path, media_type=typemap[type_tips])
        else:
            raise HTTPException(status_code=403, detail="不支持的数据类型")
    else:
        raise HTTPException(status_code=404, detail="找不到资源")

@bp.post('/migration/packup', description = "迁移的打包")
async def migrate_packup(parts: list):
    return await Assets.migration_packup(parts)

@bp.get('/migration/packup', description = "迁移的打包")
async def migrate_packup_get():
    return await Assets.migration_packup([])

@bp.get('/migration')
async def migrate_from_ip(ip: str):
    return await Assets.migration_from(ip)