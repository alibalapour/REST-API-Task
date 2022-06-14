from typing import Optional, List, Any, Union
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
import datetime


class History:
    version: str
    value: Union[int, str]  # value of corresponded version
    date: str

    def __init__(self, value) -> None:
        self.version = '1.0'
        self.value = value
        self.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')


class Item(BaseModel):
    id: Optional[UUID] = uuid4()
    key: Union[int, str]
    value: Union[int, str]   # current value
    # history: Optional[List[History]]

