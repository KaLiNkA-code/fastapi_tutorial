from typing import List, Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# HTTP PUT изменяет все значения из блока, а те значения, 
# которые не передали изменяются на default

# HTTP PATCH - операция частичного обновления данных.


# exclude_unset Использование параметра Pydantic

from typing import List, Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True) # 2
    update_item = stored_item_model.copy(update=update_data) # 1
    items[item_id] = jsonable_encoder(update_item)
    return update_item


# update - Использование параметра Pydantic
"""
1) Теперь вы можете создать копию существующей модели с помощью
.copy() и передать update параметр с dict данными для обновления

2) Это создаст dictтолько те данные, которые были установлены 
при создании item модели, за исключением значений по умолчанию.

3) Сгенерируйте dict без значений по умолчанию из 
входной модели (используя exclude_unset).

Таким образом, вы можете обновлять только значения, 
фактически установленные пользователем, вместо 
переопределения значений, уже сохраненных 
значениями по умолчанию в вашей модели.

4) Создайте копию сохраненной модели, обновив ее атрибуты 
полученными частичными обновлениями (используя updateпараметр).

5) Преобразуйте скопированную модель во что-то, 
что можно сохранить в вашей БД 
(например, с помощью файла jsonable_encoder).

(Это сравнимо с .dict() повторным использованием метода модели, 
но гарантирует (и преобразует) значения в типы данных, которые 
можно преобразовать в JSON, например, datetime в str.)
"""
