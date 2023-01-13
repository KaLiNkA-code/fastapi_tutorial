"""
Вы можете объявить тип, используемый для ответа, 
аннотировав возвращаемый тип функции операции пути .
"""
from typing import List, Union, Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []
    tag: List[str] = []
    
    
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> List[Item]:
    return [
        Item(name="Portal", price=41.0, tax=12),
        Item(name="Plumbus", price=32.0),
    ]
    
    
"""
response_model Параметр
В некоторых случаях вам нужно или вы хотите вернуть некоторые данные, 
которые не совсем соответствуют тому, что объявляет тип.
"""


@app.post("/item/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/item/", response_model=List[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


"""
response_model приоритет

Если вы объявите и возвращаемый тип, и response_model, 
то response_modelон будет иметь приоритет и использоваться FastAPI.
"""
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None
    
    
# Don't do this in pproduction!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user
