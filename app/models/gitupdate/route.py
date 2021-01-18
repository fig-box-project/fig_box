from fastapi import APIRouter, HTTPException, Body
import os

bp = APIRouter()

@bp.post("/listen")
def read(data = Body(...)):
    commit_message = data["commits"][0]["message"]
    print(commit_message)
    # 如果消息为d则删库
    if commit_message == "d":
        request = os.popen("rm -f db.sqlite")
        print(request.read())
    # pull的执行
    request = os.popen("git pull")
    pr = request.read().split("\n")[-2]
    pr = pr.split("origin/master")[-1]
    # print(pr)
    