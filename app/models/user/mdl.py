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

    character_id = Column(Integer,ForeignKey('characters.id'))
    character = relationship("Chara",back_populates = "users")

    articles = relationship("Article",back_populates='owner')
    def get_token(self,expires_in=3600):
        try:
            data = jwt.encode(
                {'id':self.id, 'exp':time.time()+expires_in},
                'my god love me forever tom', algorithm='HS256')
        except:
            return "error"
        return data
    
    
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)