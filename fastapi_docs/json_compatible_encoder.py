# JSON-совместимый кодировщик

"""
В некоторых случаях вам может потребоваться преобразовать 
тип данных (например, модель Pydantic) во что-то, 
совместимое с JSON (например dict, list, и т. д.).
"""


from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None
    
    
app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
