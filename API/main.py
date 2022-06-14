from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from models import Item, History

app = FastAPI()

db: List[Item] = [
    Item(
        key = 1,
        value = 'sfsfd',
        history = [History(
            value = 'sfsfd'
        )]
    )
]

@app.get("/")
async def read_root():
    return {"Hello There :)"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;