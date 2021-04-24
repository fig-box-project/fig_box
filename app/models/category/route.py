from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from app.models.category import orm, mdl
from app.models.mdl import database
from app.models.system import token
from app.models.user.mdl import User

bp = APIRouter()


@bp.get('/read/{id}')
def read_database(id: int, db: Session = Depends(database.get_db)):
    return db.query(mdl.Category).filter_by(id=id).first()


@bp.post('/create')
def create_category(data: orm.CategoryCU, db: Session = Depends(database.get_db),
                    now_user: User = Depends(token.check_token), ):
    data = mdl.Category(**data.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {'id': data.id}


@bp.delete('/delete')
def delete_category(id: int, db: Session = Depends(database.get_db), now_user: User = Depends(token.check_token),):
    db.query(mdl.Category).filter_by(id=id).delete()
    db.commit()


@bp.put('/update')
def update_json(id: int, data: orm.CategoryCU, db: Session = Depends(database.get_db),
                now_user: User = Depends(token.check_token), ):
    insert_data = data.dict()
    insert_data['id'] = id
    db.query(mdl.Category).update(insert_data)
    db.commit()
