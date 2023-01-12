"""
Другие типы данных


Вот некоторые из дополнительных типов данных, которые вы можете использовать:


UUID:
- Стандартный «универсальный уникальный идентификатор», 
используемый в качестве идентификатора во многих базах данных и системах.
- В запросах и ответах будет представлен в виде файла str.


datetime.datetime
- Питон datetime.datetime.
- В запросах и ответах будут 
представлены str в формате ISO 8601, например: 2008-09-15T15:53:00+05:00.


datetime.date
- Питон datetime.date.
- В запросах и ответах будут представлены
str в формате ISO 8601, например: 2008-09-15.


datetime.time
- Питон datetime.time.
- В запросах и ответах будут 
представлены str в формате ISO 8601, например: 14:23:55.003.


datetime.timedelta
- Питон datetime.timedelta.
- В запросах и ответах будет представлено floatобщее количество секунд.
- Pydantic также позволяет представить его как «кодировку разницы во времени ISO 8601»


frozenset
- В запросах и ответах обрабатываются так же, как и set:
- В запросах будет читаться список, удаляя дубликаты и преобразовывая его в файл set.
- В ответах setони будут преобразованы в list.
- В сгенерированной схеме будет указано, что set 
значения уникальны (с использованием схемы JSON uniqueItems).


bytes
- Стандартный питон bytes.
- В запросах и ответах будут рассматриваться как str.
- В сгенерированной схеме будет указано, что она имеет strформат binary.


Decimal
- Стандартный питон Decimal.
- В запросах и ответах обрабатывается так же, как float.
"""

from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID


from fastapi import Body, FastAPI


app = FastAPI()


@app.put("/items/{item_id}")
async def read_item(
    item_id: UUID,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None)
):
    
    """
    Обратите внимание, что параметры внутри функции имеют свой 
    естественный тип данных, и вы можете, например, выполнять 
    обычные манипуляции с датами, например:
    """
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
