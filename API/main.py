from typing import List, Union
from fastapi import FastAPI, HTTPException, Request, Form
from models import Item, History, ItemUpdateRequest
from datetime import datetime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='../templates/')
app = FastAPI()

db: List[Item] = [
    Item(                     # just an example
        key=1,
        value='one',
        history=[History(
            version='1.0',
            value='one',
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )]
    )
]


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse('getItemsPage.html', context={'request': request, 'result': "Hello There :)"})


@app.get("/api/v1/items")
async def fetch_items(request: Request):
    return templates.TemplateResponse('getItemsPage.html', context={'request': request, 'result': db})


@app.get('/api/v1/set')
def form_post(request: Request):
    result = 'Enter key & value'
    return templates.TemplateResponse('setItemPage.html', context={'request': request, 'result': result})


@app.post("/api/v1/set")
async def set_item(request: Request, key: Union[str, int] = Form(...), value: Union[str, int] = Form(...)):
    item = Item(key=key, value=value)

    item.history = [History(version='1.0',
                            value=value,
                            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]

    db.append(item)
    return templates.TemplateResponse('setItemPage.html', context={'request': request,
                                                                   'key': key,
                                                                   'value': value,
                                                                   'result': item.key}
                                      )


@app.delete("/api/v1/items/{key}")
async def delete_item(key: Union[str, int]):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            db.remove(item)
            return
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.put("/api/v1/items/{key}")
async def update_item(item_update: ItemUpdateRequest, key: Union[str, int]):
    for item in db:
        if item.key == key or str(item.key) == str(key):
            if item_update.value is not None:
                item.value = item_update.value                          # update value
                previous_version = float(item.history[0].version)
                item.history.insert(0, History(value=item.value,        # add history to the first of the list
                                               date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                               version=str(previous_version+1.0)))
            return
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get("/api/v1/items/{key}")
async def fetch_item_value(key):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            return item.value
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get("/api/v1/items/history/{key}")
async def fetch_item_history(key):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            return item.history
    raise HTTPException(
        status_code=404,
        detail=f'item with key: {key} was not found'
    )
