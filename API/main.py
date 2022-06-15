from typing import List, Union
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import Item, History
from datetime import datetime


app = FastAPI()

db: List[Item] = [
    Item(                     # just an example
        key = 1,
        value = 'one',
        history = [History(
            value = 'one',
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )]
    )
]

@app.get("/")
async def read_root():
    return {"Hello There :)"}


@app.get("/api/v1/users")
async def fetch_items():
    return db;


@app.post("/api/v1/users")
async def set_item(item:Item):
    item.history = [History(value = item.value,
     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]
    db.append(item)
    return {'id': item.id}
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.delete("/api/v1/users/{key}")
async def delete_item(key:Union[str, int]):
    for item in db:
        print(type(item.key), type(key))
        if item.key == key or str(item.key) == str(key):      # item.key: string & key: int
            db.remove(item)
            return
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )