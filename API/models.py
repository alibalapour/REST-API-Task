from typing import Optional, List, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class History(BaseModel):
    version: Optional[str] = '1.0'
    value: Union[int, str]  # value of corresponded version
    date: Optional[str] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


class Item(BaseModel):
    id: Optional[UUID] = uuid4()
    key: Union[int, str]
    value: Union[int, str]   # current value
    history: Optional[List[History]]

