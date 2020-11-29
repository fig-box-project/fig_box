from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.post('/write',description='写')
def write(file_path: str=Body(...), data: str=Body(...)):
    if file_path[0] != '/':
        if crud.check_path_is_dir(file_path):
            raise HTTPException(status_code=409,detail='与已存在文件夹重名')
        return crud.write(file_path, data)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.get('/ls',description='是ls 用于查看文件列表')
def ls():
    return crud.ls()

@bp.get('/read',description='读取文件内容')
def read(file_path: str):
    if file_path[0] != '/':
        return crud.read(file_path)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.post('/create',description='创建文件夹路径')
def create(directory: str=Body(...,embed=True)):
    if directory[0] != '/':
        if crud.check_path_has(directory):
            raise HTTPException(status_code=409,detail='文件或文件夹已存在')
        else:
            return crud.create_directory(directory)
    else:
        raise HTTPException(status_code=422,detail='斜杠太多')

@bp.post('/clean',description='清空空的文件夹')
def clean():
    return crud.clean()

@bp.delete('/delete',description='删除文件')
def delete(directory: str=Body(...,embed=True)):
    if crud.delete(directory):
        return True
    else:
        raise HTTPException(status_code=404,detail='找不到资源')

@bp.put('/rename',description='重命名')
def rename(old_file_path: str=Body(...), new_file_path: str=Body(...)):
    crud.rename(old_file_path,new_file_path)

# 模版功能
@bp.get('/render/test')
def render_test(request: Request):
    return crud.render_test(request)