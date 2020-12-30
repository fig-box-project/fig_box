from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get("/photo/{name}")
def photo(name: str):
    return crud.read(name)