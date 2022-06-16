from typing import List, Union
from fastapi import FastAPI, HTTPException, Request, Form
from API.models import Item, History
from datetime import datetime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates/')
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
    return templates.TemplateResponse('rootPage.html', context={'request': request, 'result': "Hello There :)"})


@app.get("/api/v1/items")
async def fetch_items(request: Request):
    return templates.TemplateResponse('getItemsPage.html', context={'request': request, 'result': db})


@app.get('/api/v1/set')
def def_page_set(request: Request):
    '''
    to create a web page for set_item part of API, first we need to send a GET request
    '''
    result = 'Enter key & value which you want to add'
    return templates.TemplateResponse('setItemPage.html', context={'request': request, 'result': result})


@app.post("/api/v1/set")
async def set_item(request: Request, key: Union[str, int] = Form(...), value: Union[str, int] = Form(...)):
    item = Item(key=key, value=value)               # creates an Item object

    item.history = [History(version='1.0',          # sets history of item
                            value=value,
                            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]

    db.append(item)                                 # adds item to database
    return templates.TemplateResponse('setItemPage.html', context={'request': request,
                                                                   'key': key,
                                                                   'value': value,
                                                                   'result': item.key}
                                      )


@app.get('/api/v1/delete')
def def_page_delete(request: Request):
    '''
    to create a web page for delete_item part of API, first we need to send a GET request
    '''
    result = 'Enter key which you want to delete'
    return templates.TemplateResponse('deleteItemPage.html', context={'request': request, 'result': result})


@app.post("/api/v1/delete")
async def delete_item(request: Request, key: Union[str, int] = Form(...)):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            db.remove(item)
            return templates.TemplateResponse('deleteItemPage.html', context={'request': request,
                                                                              'key': key,
                                                                              'result': item.key}
                                              )
    raise HTTPException(                         # raise 404 exception if key is not found
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get('/api/v1/update')
def def_page_update(request: Request):
    '''
    to create a web page for update_item part of API, first we need to send a GET request
    '''
    result = 'Enter key & value which you want to update'
    return templates.TemplateResponse('updateItemPage.html', context={'request': request, 'result': result})


@app.post("/api/v1/update")
async def update_item(request: Request, key: Union[str, int] = Form(...), value: Union[str, int] = Form(...)):
    for item in db:
        if item.key == key or str(item.key) == str(key):
            if value is not None:
                item.value = value                          # update value
                previous_version = float(item.history[0].version)
                item.history.insert(0, History(value=item.value,        # add history to the first of the list
                                               date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                               version=str(previous_version+1.0)))
            return templates.TemplateResponse('updateItemPage.html', context={'request': request,
                                                                              'key': key,
                                                                              'value': value,
                                                                              'result': item.key}
                                              )
    raise HTTPException(                      # raise 404 exception if key is not found
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get('/api/v1/fetchItem')
def def_page_fetch_item_value(request: Request):
    '''
    to create a web page for fetch_item_value part of API, first we need to send a GET request
    '''
    result = 'Enter key which you want to fetch value'
    return templates.TemplateResponse('fetchItemPage.html', context={'request': request})


@app.post("/api/v1/fetchItem")
async def fetch_item_value(request: Request, key: Union[str, int] = Form(...)):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            return templates.TemplateResponse('fetchItemPage.html', context={'request': request,
                                                                             'key': key,
                                                                             'value': item.value}
                                              )
    raise HTTPException(                     # raise 404 exception if key is not found
        status_code=404,
        detail=f'item with key: {key} was not found'
    )


@app.get('/api/v1/fetchHistory')
def def_page_fetch_item_history(request: Request):
    '''
    to create a web page for fetch_item_history part of API, first we need to send a GET request
    '''
    result = 'Enter key which you want to fetch history'
    return templates.TemplateResponse('fetchHistoryItemPage.html', context={'request': request})


@app.post("/api/v1/fetchHistory")
async def fetch_item_history(request: Request, key: Union[str, int] = Form(...)):
    for item in db:
        # item.key: string & key: int
        if item.key == key or str(item.key) == str(key):
            return templates.TemplateResponse('fetchHistoryItemPage.html', context={'request': request,
                                                                                    'key': key,
                                                                                    'history': item.history}
                                              )
    raise HTTPException(                         # raise 404 exception if key is not found
        status_code=404,
        detail=f'item with key: {key} was not found'
    )
