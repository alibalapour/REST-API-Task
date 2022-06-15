from typing import List, Union
from fastapi import FastAPI, HTTPException, Request
from models import Item, History, ItemUpdateRequest
from datetime import datetime
from fastapi.templating import Jinja2Templates


app = FastAPI()

db: List[Item] = [
    Item(                     # just an example
        key = 1,
        value = 'one',
        history = [History(
            version = '1.0',
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
    item.version = '1.0'
    item.history = [History(value = item.value,
     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]
    
    db.append(item)
    return {'id': item.id}


@app.delete("/api/v1/users/{key}")
async def delete_item(key:Union[str, int]):
    for item in db:
        if item.key == key or str(item.key) == str(key):      # item.key: string & key: int
            db.remove(item)
            return
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.put("/api/v1/users/{key}")
async def update_item(item_update:ItemUpdateRequest, key:Union[str, int]):
    for item in db:
        if item.key == key or str(item.key) == str(key):
            if item_update.value is not None:
                item.value = item_update.value                          # update value
                previous_version = float(item.history[0].version)
                item.history.insert(0, History(value = item.value,        # add history to the first of the list
                 date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 version=str(previous_version+1.0)))
            return
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get("/api/v1/users/{key}")
async def fetch_item_value(key):
    for item in db:
        if item.key == key or str(item.key) == str(key):      # item.key: string & key: int
            return item.value
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get("/api/v1/users/history/{key}")
async def fetch_item_history(key):
    for item in db:
        if item.key == key or str(item.key) == str(key):      # item.key: string & key: int
            return item.history
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )