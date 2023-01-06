from fastapi import FastAPI

app = FastAPI()


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/user")
async def rick_morty_read():
    return ['Rick', 'Morty']


@app.get("/user")
async def no_rick_morty_read():
    return ['Pick', 'Mick']