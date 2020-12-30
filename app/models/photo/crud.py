import os
from starlette.responses import FileResponse

def read(name: str):
    return FileResponse('files/photos/'+name,media_type='image/jpeg')