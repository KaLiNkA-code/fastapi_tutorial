from typing import Union


from fastapi import Body, FastAPI, Path
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None
    ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User
):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

"""
в функции выше FastAPI заметит, что используется больше 
одного параметра тела, поэтому он будет использовать имена 
параметров в качестве ключей
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
"""


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

"""
В этом случае FastAPI будет ожидать тело вида:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
"""


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

"""
embed=True
дает возможность даже у одного класса сделать имена 
параметров в качестве ключей
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
embed=False
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
"""

