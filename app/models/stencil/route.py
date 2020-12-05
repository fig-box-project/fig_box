from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get('/render/{p:path}')
def render_test(request: Request,p:str):
    return crud.render_test(request,p)