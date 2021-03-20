from pydantic import BaseModel

class PhotoUpload(BaseModel):
    name: str

class Photo(PhotoUpload):
    class Config:
        orm_mode= True