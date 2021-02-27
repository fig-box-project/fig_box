from fastapi.exceptions import HTTPException
from app.models.settings.crud import settings
from . import orm

# 分辨器
class Recognizer:
    cache = {1:{1},2:{8}}
    def check_auth(self,chara:int, auth:int):
        if chara == 1:
            return True
        return auth in self.cache[chara]
recognizer = Recognizer()

auth_data = settings.value["character"]["auth_numbers"]
chara_data = settings.value["character"]["charas"]

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
        raise HTTPException(status_code=400,detail="abc")
        
def delete(name:str):
	

