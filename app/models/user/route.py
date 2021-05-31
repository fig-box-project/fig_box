from fastapi import APIRouter, HTTPException, Depends
from html_builder import Html
from sqlalchemy.orm import Session
from starlette.requests import Request

from . import orm, crud, mdl
from app.models.mdl import database
from .crud import UserCrud
from ..page.crud import PageRouter, ParamsContainer, RequestItem
from ..system.check_token import token
from ..tools import GetListDepend


def user_api_route(bp):
    @bp.get('/check', description='检查用户名是否存在')
    def check(username, db: Session = Depends(database.get_db)):
        if not UserCrud.check_user_name(db, username):
            return '不存在,可注册'
        else:
            raise HTTPException(status_code=404, detail='存在')

    @bp.post('/register', description='注册', response_model=orm.User)
    def create_user(user: orm.UserCreate,
                    request: Request,
                    db: Session = Depends(database.get_db), ):
        if not UserCrud.check_user_name(db, user.username):
            return UserCrud.create_user(db, user, request)
        else:
            raise HTTPException(status_code=409, detail='用户已存在')

    @bp.post('/login', description='登录')
    def login(user: orm.UserLogin, db: Session = Depends(database.get_db)):
        b, token = UserCrud.login_user(db, user)
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

    @bp.get('/view/ls', description='查看所有用户')
    def view_all_user(
            ls_depend: GetListDepend = Depends(),
            user: mdl.UserMdl = Depends(token.check_token),
            db: Session = Depends(database.get_db)):
        user.into_auth("user_all_edit")
        return ls_depend.get_request(db, mdl.UserMdl)

    @bp.get('/profile', description='获取用户主页信息,api')
    def profile_data(
            user: mdl.UserMdl = Depends(token.check_token)
            , db: Session = Depends(database.get_db)):
        return user

    # @bp.get('/logs', description='获取用户log')
    # def get_logs():
    #     with open('')


def user_page_route(pg_bp, p):
    def profile_creator():
        rt = Html('用户页面')
        rt.body.addElement('名称 {{ user.username }} ')
        return rt

    @pg_bp.get('/profile/{params:path}', description='对外显示的用户profile(用户信息首页),输入ID')
    @p.wrap()
    def profile_page(pc: ParamsContainer, id: str):
        id = int(id)
        if id > 2:
            user = pc.db.query(mdl.UserMdl).get(id)
            if user is None:
                # return 404, '找不到用户'
                return RequestItem.with404('找不到用户')
            data = {'user': user}
            return RequestItem('user/profile.html', data, profile_creator)
        raise HTTPException(403, '权限不足')
