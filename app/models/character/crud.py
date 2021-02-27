from app.models.settings.crud import settings

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
def creat_character(name:str, auths:str, description:str):
	if name != "" and name not in chara_data:
		
		auths = 
		chara_data[name] = {
			
		}
    
    


# def get_chara(db: Session, id: int):
#     return db.query(mdl.Chara).filter(mdl.Chara.id == id).first()

# def get_charas(db: Session, skip = 0, limit=100):
#     return db.query(mdl.Chara).offset(skip).limit(limit).all()

# def create(db: Session,chara_data: orm.CharaBases):
#     new_chara = mdl.Chara(**chara_data.dict())
#     db.add(new_chara)
#     db.commit()
#     db.refresh(new_chara)
#     return new_chara

# def update(db: Session, chara_data: orm.CharaUpdate):
#     db.query(mdl.Chara).filter(mdl.Chara.id == chara_data.id).update(chara_data.dict())
#     db.flush()
#     db.cpmmit()
#     return True

# def delete(db: Session, id: int):
#     chara = db.query(mdl.Chara).filter(mdl.Chara.id == id).first()
#     if chara:
#         db.delete(chara)
#         # 只提交到缓存
#         db.commit()
#         return chara