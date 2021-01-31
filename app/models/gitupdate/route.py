from fastapi import APIRouter, HTTPException, Body
from ..packager.crud import packager
import os

bp = APIRouter()

@bp.post("/listen",description="TODO:拒绝从github以外的来源")
def read(data = Body(...)):
    commit_message = data["commits"][0]["message"]
    print(commit_message)
    # 用空格分开以处理各种请求
    c_m_list = commit_message.split(" ")

    # 如果消息为d则删库
    if "d" in c_m_list:
        request = os.popen("rm -f db.sqlite")
        print(request.read())

    # 更新Python包,在import前先录入和更新好
    if "p" in c_m_list:
        request = os.popen("pip3 install -r requirements.txt")
        print(request.read())

    # 备份各样东西
    packager.dump()

    # pull的执行
    if "u" in c_m_list or "u\n" in c_m_list:
        request = os.popen("git pull --ff-only")
    
