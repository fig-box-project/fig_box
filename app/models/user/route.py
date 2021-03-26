from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import orm, crud, mdl
from app.models.mdl import database
from app.main import check_token

bp = APIRouter()

@bp.get('/check',description='')
def check(username,db: Session=Depends(database.get_db)):
    if not crud.isloged_user(db,username):
        return '不存在'
    else:
        raise HTTPException(status_code=404,detail='存在')

@bp.post('/register',description='注册',response_model=orm.User)
def create_user(user:orm.UserCreate,db: Session=Depends(database.get_db)):
    if crud.isloged_user(db,user.username) == False:
        return crud.create_user(db,user)
    else:
        raise HTTPException(status_code=409,detail='User already exists')

@bp.post('/login',description='登录')
def login(user:orm.UserLogin,db: Session=Depends(database.get_db)):
    b,token = crud.login_user(db,user)
    if b:
        return {'token':token}
    else:
        raise HTTPException(status_code=404,detail=token)

# @bp.put('/update',description='更新其它用户的资料权限等')
# def update(
#     aim_user:orm.UserUpdate,
#     user:mdl.User = Depends(check_token),
#     db: Session=Depends(database.get_db)):
#     user.into_auth("user_all_edit")
#     return crud.update_user_character(db,aim_user)

@bp.get('/view/all_user',description='查看所有用户')
def view_all_user(
    user:mdl.User = Depends(check_token),
    db: Session=Depends(database.get_db)):
    user.into_auth("user_all_edit")
    return crud.get_users(db)