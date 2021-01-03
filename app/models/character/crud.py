from sqlalchemy.orm import Session
from . import mdl, orm


# 分辨器
class Recognizer:
    cache = {1:{1},2:{8}}
    def check_auth(self,chara:int, auth:int):
        if chara == 1:
            return True
        return auth in self.cache[chara]

def get_chara(db: Session, id: int):
    return db.query(mdl.Chara).filter(mdl.Chara.id == id).first()

def get_charas(db: Session, skip = 0, limit=100):
    return db.query(mdl.Chara).offset(skip).limit(limit).all()

def create(db: Session,chara_data: orm.CharaBases):
    new_chara = mdl.Chara(**chara_data.dict())
    db.add(new_chara)
    db.commit()
    db.refresh(new_chara)
    return new_chara

def update(db: Session, chara_data: orm.CharaUpdate):
    db.query(mdl.Chara).filter(mdl.Chara.id == chara_data.id).update(chara_data.dict())
    db.flush()
    db.cpmmit()
    return True

def delete(db: Session, id: int):
    chara = db.query(mdl.Chara).filter(mdl.Chara.id == id).first()
    if chara:
        db.delete(chara)
        # 只提交到缓存
        db.commit()
        return chara