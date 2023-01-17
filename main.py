# Запросить файлы

"""
Вы можете определить файлы, которые должны 
быть загружены клиентом, используя файлы File
"""


from fastapi import FastAPI, File, UploadFile


app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("uploadfile")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# Определить File параметры