from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base
from app.models.character.crud import recognizer
import jwt,time

from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    id              = Column(Integer, primary_key=True)
    username        = Column(String(32), index=True)
    password_hash   = Column(String(128))

    character_id    = Column(Integer, default=2)

    def get_token(self,expires_in=3600):
        try:
            data = jwt.encode(
                {'id':self.id, 'exp':time.time()+expires_in},
                'my god love me forever tom', algorithm='HS256')
        except:
            return "error"
        return data
    
    # 检查权限,auth请输入权限代号
    def check_auth(self,auth:int):
        return recognizer.check_auth(self.character_id,auth)
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
