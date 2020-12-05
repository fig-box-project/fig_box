from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, orm
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.post('/install')
def install(module:orm.Module):
    return crud.install_module(module)