from typing import Union

from fastapi import FastAPI, Path, Query


app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
    ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    """Тоже самое, что и предыдущее"""
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get", ge=1), q: str):
    """ge=1 означает, что число должно быть целым и больше 1"""
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""
ge = greater than or equal (Больше или равно)
gt = greater than (Больше, чем)
le = less than or equal (Меньше или равно)
lt = less than (Меньше, чем)
"""


@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get", gt=0, le=1000), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



@app.get("/item/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(qt=0, lt=10.5)      
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
