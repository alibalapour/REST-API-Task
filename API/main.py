from typing import List
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
async def set_items(item:Item):
    item.history = [History(value = item.value,
     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]
    db.append(item)
    return {'id': item.id}
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')