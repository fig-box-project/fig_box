from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud
import app.conf as conf
from app.main import check_token
from app.models.user.mdl import User
import os
bp = APIRouter()


# @bp.post('/file/upload',description = '上传文件')
# async def upload(file_path: str=Body(...),file: UploadFile = File(...)):
#     rt = await crud.editor.create_file(file,file_path)
#     if rt == None:
#         raise HTTPException(status_code=404,detail='路径不存在')
#     else:
#         return rt

@bp.get('/templates/link')
def get_link():
    return conf.domain_port + "/api/v1/editor/packup/templates"
    
@bp.post('/write',description='写')
def write(file_path: str=Body(...), data: str=Body(...)):
    if file_path[0] != '/':
        if crud.editor.check_path_is_dir(file_path):
            raise HTTPException(status_code=409,detail='与已存在文件夹重名')
        return crud.editor.write(file_path, data)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.get('/ls',description='是ls 用于查看文件列表')
def ls():
    rt = crud.editor.ls()
    if rt != None:
        return rt
    else:
        raise HTTPException(status_code=404)

@bp.get('/read',description='读取文件内容')
def read(file_path: str):
    if file_path[0] != '/':
        return crud.editor.read(file_path)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.post('/create',description='创建文件夹路径')
def create(directory: str=Body(...,embed=True)):
    if directory[0] != '/':
        if os.path.exists(directory):
            raise HTTPException(status_code=409,detail='文件或文件夹已存在')
        else:
            return crud.editor.create_directory(directory)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.delete('/delete/directory',description='删除一个空的文件夹')
def delete_directory(directory: str):
    if crud.editor.delete_directory(directory):
        return True
    else:
        raise HTTPException(status_code=403,detail='权限不足')

@bp.delete('/delete',description='删除文件')
def delete(file_path: str):
    if crud.editor.delete(file_path):
        return True
    else:
        raise HTTPException(status_code=404,detail='找不到资源')

@bp.put('/rename',description='重命名')
def rename(old_file_path: str=Body(...), new_file_path: str=Body(...)):
    crud.editor.rename(old_file_path,new_file_path)

