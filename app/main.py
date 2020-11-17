from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'state':'successss'}

@app.get("/items/{item_id}",tags=['items'])
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}