from fastapi import APIRouter, HTTPException, Body
from ..packager.crud import packager
import os

bp = APIRouter()

@bp.post("/listen",description="TODO:拒绝从github以外的来源")
def read(data = Body(...)):
    commit_message = data["commits"][0]["message"]
    print(commit_message)
    # 如果消息为d则删库
    if commit_message == "d":
        request = os.popen("rm -f db.sqlite")
        print(request.read())

    # 更新Python包,在import前先录入和更新好
    if commit_message == "p":
        request = os.popen("pip3 install -r requirements.txt")
        print(request.read())
    # 备份各样东西
    packager.dump()
    # pull的执行
    request = os.popen("git pull --ff-only")
    
@bp.post("/blog",description="TODO:拒绝从github以外的来源")
def read(data = Body(...)):
    os.popen("cd /www/wwwroot/test.leesinhao.com/blog")
    request = os.popen("git pull --ff-only")