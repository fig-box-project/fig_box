from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get("/read/{name}")
def read(name: str):
    return crud.jsaver.read(name)

@bp.post("/write")
def write(name: str, json_str: str):
    crud.jsaver.write(name, json_str)