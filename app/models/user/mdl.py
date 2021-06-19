from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

# from app.models.character import CharacterMdl
from app.models.mdl.database import Base
from app.models.settings.crud import settings
import jwt
import time

from werkzeug.security import generate_password_hash, check_password_hash


class UserMdl(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))

    birth_date = Column(DateTime)

    character_id = Column(Integer, ForeignKey('character.id'))
    character = relationship('CharacterMdl', back_populates='users')

    def get_token(self, expires_in=3600):
        try:
            data = jwt.encode(
                {'id': self.id, 'exp': time.time() + expires_in},
                settings.value['token_key'], algorithm='HS256')
        except:
            return "error"
        return data

    # 检查权限,auth请输入权限符
    def into_auth(self, auth: str):
        """检查权限,auth请输入权限符,如果此用户没有此权限将抛出403"""
        # TODO: 修复检查角色的功能
        # if not check_auth(self.character, auth):
        #     raise HTTPException(
        #         status_code=403, detail='用户权限不足,不能进入 ' + auth + ' 权限')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
