# # Запросить файлы

# """
# Вы можете определить файлы, которые должны 
# быть загружены клиентом, используя файлы File
# """


# from fastapi import FastAPI, File, UploadFile

# from typing import Union


# app = FastAPI()


# @app.post("/files/")
# async def create_file(file: bytes = File()):
#     return {"file_size": len(file)}


# @app.post("uploadfile")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}


# """
# UploadFile имеет следующие атрибуты:

# filename: str с исходным именем загруженного файла (например, myimage.jpg).

# content_type: str с типом содержимого (тип MIME / тип носителя) (например, image/jpeg).

# file: АSpooledTemporaryFile Это фактический файл Python, который вы можете передать напрямую 
# другим функциям или библиотекам, которые ожидают объект, похожий на файл.
# """


# """
# UploadFile имеет следующие async методы. Все они вызывают соответствующие 
# файловые методы внизу (используя внутренний SpooledTemporaryFile).

# write(data): Записывает data(str или bytes) в файл.

# read(size): Читает size(int) байт/символов файла.

# seek(offset): Переход к позиции байта offset(int) в файле.

# Например, await myfile.seek(0)перейдет к началу файла.
# Это особенно полезно, если вы запускаете await myfile.read()один раз, 
# а затем вам нужно снова прочитать содержимое.

# close(): Закрывает файл.
# """
# """
# если функция асинхронная:
# contents = await myfile.read()

# если просто def:
# contents = myfile.file.read()
# """


# #  Необязательная загрузка файла


# @app.post("/files/")
# async def create_file(file: Union[bytes, None] = File(default=None)):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}
    
    
# @app.post("/uploadfile/")
# async def create_upload_file(file: Union[UploadFile, None] = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}


# # UploadFile с дополнительными метаданными
# @app.post("/uploadfile/")
# async def create_upload_file(file: bytes = File(description="A file read as bytes"):
#     return {"filename": file.filename}


from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.post("/files/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile")):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
    <body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
