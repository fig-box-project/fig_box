from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud, orm
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get("/read/{name}")
def read(name: str):
    return crud.jsaver.read(name)

@bp.post("/write")
def write(data:orm.JsaverWrite):
    crud.jsaver.write(data.name, data.json_str)