from typing import Union, List
from fastapi import FastAPI, Header


app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}


# Header автоматически конвертирует user_agent в User-Agent
# Это можно отключить добавив аргумент в функцию: convert_underscores=False


@app.get("/items/")
async def read_items(strange_header: Union[str, None] = Header(default=None, convert_underscores=False)):
    return {"strange_header": strange_header}


# Дублирующиеся заголовки

"""
Например, чтобы объявить заголовок X-Token, который может появляться более одного раза, вы можете написать:
"""


@app.get("/items/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {"X-Token values": x_token}


"""
X-Token: foo
X-Token: bar

Ответ будет таким
{
    "X-Token values": [
        "bar",
        "foo"
    ]
}
"""