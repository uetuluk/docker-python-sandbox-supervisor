from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from container import create_container, check_container, upload_file, download_file
import requests


class Code(BaseModel):
    code_string: str


class Container(BaseModel):
    instance_id: str | None = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

user = {"container": {}}


@app.post("/container")
async def container(container: Container):
    print(container)

    container_id = container.instance_id

    # create container if container_id is None
    if container_id is None:

        container_info = await create_container()
        container_id = container_info["container_id"]

    # check if container exists
    container_info = await check_container(container_id)
    user["container"] = container_info

    print(container_info)
    return "OK"


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    try:
        container_id = user["container"]["container_id"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    await upload_file(container_id, file)
    return "OK"


@app.get("/downloadfile")
async def create_download_file(file_name: str):
    try:
        container_id = user["container"]["container_id"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    file_response = await download_file(container_id, file_name)

    return file_response


@app.post("/run")
async def sandbox_run(code: Code):
    try:
        container_id = user["container"]["container_id"]
        container_port = user["container"]["container_port"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    code = jsonable_encoder(code)
    code_string = code.get("code_string")

    container_url = f"http://localhost:{container_port}/run"

    data = {
        "code_string": code_string
    }

    container_response = requests.post(container_url, json=data)

    return container_response.json()
