# данные форм

"""
Когда вам нужно получить поля формы вместо JSON, вы можете использовать Form
"""


from fastapi import FastAPI, Form


app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# Определить Form параметры
"""
Создайте параметры формы так же, как для Body или Query:
"""


# О «Полях формы»

"""
Способ, которым формы HTML ( <form></form>) отправляют данные на сервер,
обычно использует «специальную» кодировку для этих данных, 
она отличается от JSON.

FastAPI обязательно прочитает эти данные из нужного места, а не из JSON.
"""