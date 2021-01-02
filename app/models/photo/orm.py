from typing import List, Optional
from fastapi import File, UploadFile
from pydantic import BaseModel

class PhotoUpload(BaseModel):
    name: str

class Photo(PhotoUpload):
    class Config:
        orm_mode= True