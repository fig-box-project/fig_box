from fastapi import APIRouter, HTTPException, Body
from starlette.responses import FileResponse
from . import crud
import os

bp = APIRouter()

@bp.get("/download/{package_name}.zip",description="下载某个打包,大文件时需要用户权限")
def packup(package_name: str):
    crud.packager.pack(package_name)
    return FileResponse('files/packager/{}.zip'.format(package_name),media_type='application/zip')
