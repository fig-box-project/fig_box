from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, orm
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get('/test',description='测试用,毫无作用')
def test():
    return 'test'