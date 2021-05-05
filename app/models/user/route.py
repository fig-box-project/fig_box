from fastapi import APIRouter, HTTPException, Depends
from html_builder import Html
from sqlalchemy.orm import Session
from . import orm, crud, mdl
from app.models.mdl import database
from app.models.system import token
from ..page.crud import Page
from ..template.Template import Template

bp = APIRouter()


@bp.get('/check', description='检查用户名是否存在')
def check(username, db: Session = Depends(database.get_db)):
    if not crud.isloged_user(db, username):
        return '不存在,可注册'
    else:
        raise HTTPException(status_code=404, detail='存在')


@bp.post('/register', description='注册', response_model=orm.User)
def create_user(user: orm.UserCreate, db: Session = Depends(database.get_db)):
    if not crud.isloged_user(db, user.username):
        return crud.create_user(db, user)
    else:
        raise HTTPException(status_code=409, detail='User already exists')


@bp.post('/login', description='登录')
def login(user: orm.UserLogin, db: Session = Depends(database.get_db)):
    b, token = crud.login_user(db, user)
    if b:
        return {'token': token}
    else:
        raise HTTPException(status_code=404, detail=token)


# @bp.put('/update',description='更新其它用户的资料权限等')
# def update(
#     aim_user:orm.UserUpdate,
#     user:mdl.User = Depends(check_token),
#     db: Session=Depends(database.get_db)):
#     user.into_auth("user_all_edit")
#     return crud.update_user_character(db,aim_user)


@bp.get('/view/all_user', description='查看所有用户')
def view_all_user(
        user: mdl.User = Depends(token.check_token),
        db: Session = Depends(database.get_db)):
    user.into_auth("user_all_edit")
    return crud.get_users(db)


@bp.get('/profile', description='获取用户主页信息,api')
def profile_data(
        user: mdl.User = Depends(token.check_token)
        , db: Session = Depends(database.get_db)):
    return user


pg_bp = APIRouter()
p = Page()


def profile_creator():
    rt = Html('用户页面')
    rt.body.addElement('欢迎 {{ user.username }} 光临')
    return rt


@pg_bp.get('/profile/{params:path}', description='对外显示的用户页面')
@p.wrap()
def profile_page(db: Session, id: str):
    id = int(id)
    if id > 2:
        user = db.query(mdl.User).get(id)
        if user is None:
            return 404, '找不到用户'
        data = {'user': user}
        return 'user/profile.html', data, profile_creator
    raise HTTPException(403, '权限不足')
