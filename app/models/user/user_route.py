from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import app.models.user.user_orm as orm
import app.models.user.user_crud as crud
from app.models import database

router = APIRouter()



# 注册
@router.post('/register',response_model=orm.User)
def create_user(user:orm.UserCreate,db: Session=Depends(database.get_db)):
    if crud.isloged_user(db,user.username) == False:
        return crud.create_user(db,user)
    else:
        raise HTTPException(status_code=400,detail='User already exists')

# 登录
@router.post('/login')
def login(user:orm.UserCreate,db: Session=Depends(database.get_db)):
    b,token = crud.login_user(db,user)
    if b:
        return {'token':token}
    else:
        raise HTTPException(status_code=404,detail=token)
