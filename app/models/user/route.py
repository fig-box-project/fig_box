from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import orm, crud, mdl
from app.models import database
from app.main import check_token

bp = APIRouter()



# 注册
@bp.post('/register',response_model=orm.User)
def create_user(user:orm.UserCreate,db: Session=Depends(database.get_db)):
    if crud.isloged_user(db,user.username) == False:
        return crud.create_user(db,user)
    else:
        raise HTTPException(status_code=400,detail='User already exists')

# 登录
@bp.post('/login')
def login(user:orm.UserCreate,db: Session=Depends(database.get_db)):
    b,token = crud.login_user(db,user)
    if b:
        return {'token':token}
    else:
        raise HTTPException(status_code=404,detail=token)

@bp.post('/update',description='更新其它用户的资料权限等')
def update(
    aim_user:orm.UserCreate,
    now_user:mdl.User = Depends(check_token),
    db: Session=Depends(database.get_db)):
    if now_user.character.can_edit_auth:
        return crud.update_user_character(db,aim_user)
    else:
        raise HTTPException(status_code=403,detail='权限不足')