from fastapi import APIRouter, HTTPException, Depends,Header,Body
from . import crud
from app.main import check_token
from app.models.user.user import User
bp = APIRouter()

@bp.post('/write/{file_path:path}',description='写')
def write(file_path: str, data: str=Body(...)):
    if file_path[0] == '/':
        return crud.write(file_path, data)
    else:
        raise HTTPException(status_code=422,detail='注意是两个斜杠')

@bp.get('/ls',description='是ls 用于查看文件列表')
def ls():
    return crud.ls()

@bp.get('/read/{file_path:path}',description='读取文件内容')
def read(file_path: str):
    if file_path[0] == '/':
        return crud.read(file_path)
    else:
        raise HTTPException(status_code=422,detail='注意是两个斜杠')

@bp.post('/create/{directory:path}',description='创建文件夹路径')
def create(directory: str):
    if directory[0] == '/':
        return crud.create_directory(directory)
    else:
        raise HTTPException(status_code=422,detail='注意是两个斜杠')

@bp.post('/clean',description='清空空的文件夹')
def clean():
    return crud.clean()