from fastapi.exceptions import HTTPException
from app.models.settings.crud import settings
from . import orm

auth_data = settings.value["character"]["auths"]
chara_data = settings.value["character"]["charas"]
default_cahara = ["master", "normal"]

# 检查角色权限
def check_auth(chara:str, auth: str):
    if chara == "master":
        return True
    else:
        # if default in chara`s auths, check auth is true default
        if "default" in chara_data[chara]["auths"]:
            return auth_data[auth]["default"]
        return auth in chara_data[chara]["auths"]

def get_auths():
    rt = []
    for k,v in auth_data.items():
        rt.append({"id":k, "description":v["description"]})
    return rt
    
def get_charas():
    rt = []
    for k,v in chara_data.items():
        rt.append({
            "name":k, 
            "auths":v["auths"],
            "description":v["description"]
        })
    return rt
    
# to create a character, auths is a str and need to  
def creat_character(chara: orm.CharaCreate):
    if chara.name != "" and chara.name not in chara_data:
        auths = []
        chara_data[chara.name] = {
            "auths":auths,
            "description":chara.description,
        }
        settings.value["character"]["charas"] = chara_data
        settings.update()
        return chara.name
    else:
        raise HTTPException(403, "name exists or none")
        
def delete(name:str):
    # can not delete default chara
    if name in default_cahara:
        raise HTTPException(403, "can not edit default chara")
    if name in chara_data:
        del chara_data[name]
        return "success"
    else:
        raise HTTPException(404, "can not find name in chara datas")
    
# remove the auth from character
def remove_one(data: orm.CharaOne):
    # can not delete default chara
    if data.name in default_cahara:
        raise HTTPException(403, "can not edit default chara")
    if data.name in chara_data:
        if data.auth in chara_data[data.name]["auths"]:
            chara_data[data.name]["auths"].remove(data.auth)
            return "success"
        else:
            return "-unExits-"
    else:
        raise HTTPException(404, "can not find name in chara datas")
        
# add one auth into character        
def add_one(data: orm.CharaOne):
    # can not delete default chara
    if data.name in default_cahara:
        raise HTTPException(403, "can not edit default chara")
    if data.name in chara_data:
        chara_data[data.name]["auths"].append(data.auth)
        return "success"
    else:
        raise HTTPException(404, "can not find name in chara datas")






