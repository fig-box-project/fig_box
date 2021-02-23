from fastapi import APIRouter, HTTPException, Body
from ..packager.crud import packager
import os

bp = APIRouter()

@bp.post("/listen",description="TODO:拒绝从github以外的来源")
def read(data = Body(...)):
    commit_message = data["commits"][0]["message"]
    print(commit_message)

    # 如果消息为d则删库
    if "del_db" in commit_message:
        request = os.popen("rm -f db.sqlite")
        print("删除数据库")

    # delete
    if "del_settings" in commit_message:
        request = os.popen("rm -f settings.yml")
        print("删除settings")

    # 更新Python包,在import前先录入和更新好
    if "pk_update" in commit_message:
        request = os.popen("pip3 install -r requirements.txt")
        print(request.read())
    # 备份各样东西
    # packager.dump()

    # 
    if "un_update" not in commit_message:
        print("不更新")
        # pull的执行
        request = os.popen("git pull --ff-only")
    
    
@bp.post("/blog",description="TODO:拒绝从github以外的来源")
def read(data = Body(...)):
    # os.popen("cd /www/wwwroot/test.leesinhao.com/Blog")
    request = os.popen("git -C /www/wwwroot/test.leesinhao.com/Blog pull")
    print(request.read())