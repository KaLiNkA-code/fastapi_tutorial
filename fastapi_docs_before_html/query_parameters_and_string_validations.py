from typing import Union, List
from pydantic import Required
from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default="fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: str = Query(min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: str = Query(default=..., min_length=3)):
    """Пораметер default с 3 точками для явного указания, что значение требуется"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=..., min_length=3)):
    """Все равно пораметр q обязательный"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=Required, min_length=3)):
    """Это аналог предыдущей функции"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(q: Union[List[str], None] = Query(default=None)):
    """list, как аргумент функции"""
    query_items = {"q": q}
    return query_items


@app.get("/items/")
async def read_items(q: Union[List[str], None] = Query(default=["value1", "value2"])):
    """default значение (список)"""
    query_items = {"q": q}
    return query_items


@app.get("/items/")
async def read_items(
    q: Union[List[str], None] = Query(default=["value1", "value2"],
                                      title="Query string",
                                      description="Query string for the items to search in the database that have a good match",
                                      min_length=3,
                                      )
):
    """добавляем пояснение функции"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(
    q: Union[List[str], None] = Query(default=["value1", "value2"], 
                                      alias="item-query",  # Вот он
                                      title="Query string",
                                      description="Query string for the items to search in the database that have a good match",
                                      min_length=3,
                                      )
):
    """alias - псевдоним для q"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(
    q: Union[List[str], None] = Query(default=["value1", "value2"], 
                                      alias="item-query",  # Вот он
                                      title="Query string",
                                      description="Query string for the items to search in the database that have a good match",
                                      min_length=3,
                                      deprecated=True,
                                      )
):
    """deprecated=True указывает, что параметр устарел"""
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/item/")
async def read_items(
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)):
    """Чтобы исключить параметр запроса из сгенерированной схемы OpenAPI: include_in_schema=False"""
    if hidden_query:
        return {"hideen_query": hidden_query}
    else:
        return {"hideen_query": "Not found"}
