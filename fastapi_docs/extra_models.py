from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None
    
    
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    
    
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None
    
    
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_id: UserIn):
    user_saved = fake_save_user(user_id)
    return user_saved


"""
example of code:

user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
user_dict = user_in.dict()
print(user_dict)

{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
"""
# Разворачивание dict
"""
UserInDB(**user_dict)

UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
or
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
"""


# Модель Pydantic из содержимого другого

"""
user_dict = user_in.dict()
UserInDB(**user_dict)

Эквивалентен

UserInDB(**user_in.dict())
"""


# Развертка dict и дополнительные ключевые слова

"""
Если мы хотим добавить доп аргумент, например хешированный пароль, то мы поступаем так:

UserInDB(**user_in.dict(), hashed_password=hashed_password)

Получаем:

UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
"""


# Уменьшить дублирование

"""
Мы можем объявить UserBaseмодель, которая служит базой для других наших 
моделей. И затем мы можем создать подклассы этой модели, которые наследуют 
ее атрибуты (объявления типов, проверка и т. д.).

Все преобразования данных, проверка, документация и т. д. будут по-прежнему 
работать в обычном режиме.

Таким образом, мы можем объявить только различия между моделями 
(с открытым текстом password, с hashed_passwordпаролем и без):
"""


from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    
    
class UserId(UserBase):
    password: str
    
    
class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
    
    
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/post/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# Union или anyOf

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# Список моделей


class Item(BaseModel):
    name: str
    description: str
    
    
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items


# Ответ с произвольным dict

"""
Вы также можете объявить ответ, используя обычный произвольный dict, 
объявляя только тип ключей и значений, не используя модель Pydantic.

Это полезно, если вы заранее не знаете допустимые имена полей/атрибутов 
(которые потребуются для модели Pydantic).

В этом случае вы можете использовать typing.Dict
"""
from typing import Dict

from fastapi import FastAPI


app = FastAPI()


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weight():
    return {"foo": 2.3, "bar": 3.4}
