"""
Вы можете объявить тип, используемый для ответа, 
аннотировав возвращаемый тип функции операции пути .
"""
from typing import List, Union, Any

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
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
    
    
# Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user


"""
another example 
"""

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None
    

class UserOut(BaseModel):
    username: str
    emain: EmailStr
    full_name: Union[str, None] = None
    
    
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


"""
Тип возвращаемого значения и фильтрация данных

Но в большинстве случаев, когда нам нужно сделать что-то подобное, 
мы хотим, чтобы модель просто фильтровала/удаляла некоторые данные, как в этом примере.

И в этих случаях мы можем использовать классы и наследование, 
чтобы воспользоваться преимуществами аннотаций типов функций, чтобы получить лучшую поддержку 
в редакторе и инструментах, и при этом получить фильтрацию данных FastAPI .
"""


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    

class UserIn(BaseModel):
    password: str
    
    
@app.post("/user/")
async def create_user(user: UserIn) -> UserOut:
    return user


"""
Аннотации других возвращаемых типов
"""

# Вернуть ответ напрямую
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


"""
Этот простой случай обрабатывается FastAPI автоматически, 
поскольку аннотация типа возвращаемого значения является классом (или подклассом) Response.

И инструменты тоже будут довольны, потому что оба RedirectResponse и 
JSONResponse являются подклассами Response, так что аннотация типа правильная.
"""


# Аннотировать подкласс ответа

@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# Недопустимые аннотации возвращаемого типа

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Union[Response, dict]:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


"""
...это не удается, потому что аннотация типа не является типом Pydantic и не является просто 
одним Responseклассом или подклассом, это союз (любой из двух) между a Responseи a dict.
"""


# Отключить модель ответа

"""
вы можете отключить генерацию модели ответа, установив response_model=None
"""


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Union[Response, dict]:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


"""
Это заставит FastAPI пропустить генерацию модели ответа, и таким 
образом вы сможете иметь любые аннотации возвращаемого типа, 
которые вам нужны, не влияя на ваше приложение FastAPI. 🤓
"""


# Параметры кодирования модели ответа


"""
с помощью response_model_exclude_unset мы можем не добавлять колонки с
данными, которые имеют значения по умолчанию
"""

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []
    
    
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


"""
на item 'foo'
{
    "name": "Foo",
    "price": 50.2
}
"""

# Используйте response_model_exclude_unset параметр (На верху)


# Данные со значениями для полей со значениями по умолчанию

"""
Но если ваши данные имеют значения для полей модели со значениями по 
умолчанию, например элемент с идентификатором bar:
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}

они будут включены в ответ.
"""


# Данные с теми же значениями, что и по умолчанию

"""
Если данные имеют те же значения, что и значения по умолчанию, 
например элемент с идентификатором baz:
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
FastAPI достаточно умен (на самом деле, Pydantic достаточно умен), 
чтобы понять, что хотя description, tax, и tags имеют те же значения, 
что и значения по умолчанию, они были заданы явно 
(а не взяты из значений по умолчанию)

Таким образом, они будут включены в ответ JSON.
"""


# response_model_include и response_model_exclude

"""
!!!Но все же рекомендуется использовать идеи выше, !!!
!!! используя несколько классов, вместо этих параметров.!!!

(Это связано с тем, что схема JSON, сгенерированная в OpenAPI 
вашего приложения (и в документации), по-прежнему будет использоваться 
для полной модели, даже если вы используете response_model_include или 
response_model_excludeопускаете некоторые атрибуты. Это касается и 
response_model_by_aliasтого, что работает аналогично)

Вы также можете использовать параметры декоратора операции 
пути response_model_include и файлы response_model_exclude.

Они берут a setс str именем атрибутов, которые нужно включить 
(исключая остальные) или исключить (включая остальные).

Это можно использовать как быстрый способ, если у вас есть только 
одна модель Pydantic и вы хотите удалить некоторые данные из вывода.
"""


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


"""
Синтаксис {"name", "description"}создает setс этими двумя значениями.

Это эквивалентно set(["name", "description"]).
"""
