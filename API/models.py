from typing import Optional, List, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class History(BaseModel):
    version: str
    value: Union[int, str]  # value of corresponded version
    date: str


class Item(BaseModel):
    id: Optional[UUID] = uuid4()
    key: Union[int, str]
    value: Union[int, str]   # current value
    history: Optional[List[History]]


class ItemUpdateRequest(BaseModel):
    key: Optional[Union[int, str]]
    value: Optional[Union[int, str]]   # current value