from fastapi import APIRouter, HTTPException, Body
import os

bp = APIRouter()

@bp.post("/git/listen")
def read(name: str):
    codes = [
        "git pull"
    ]
    for code in codes:
        request = os.popen(code)
        print(request.read())