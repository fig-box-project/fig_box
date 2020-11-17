from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base
import jwt,time

from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))

    character_id = Column(Integer,ForeignKey("character.id"))
    character = relationship("Character",back_populates = "users")

    def get_token(self,expires_in=3600):
        try:
            data = jwt.encode(
                {'id':self.id, 'exp':time.time()+expires_in},
                'my god love me forever tom', algorithm='HS256')
        except:
            return "error"
        return data
    
    # 验证token
    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, 'my god love me forever tom',
                              algorithms=['HS256'])
        except:
            return None
        return data['id']
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

