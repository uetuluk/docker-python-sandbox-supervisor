from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from container import create_container, check_container, upload_file, download_file
import requests
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from uuid import uuid4
from typing import Annotated


class Code(BaseModel):
    code_string: str


class Container(BaseModel):
    instance_id: str | None = None


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token")  # Define where to get token

user_db = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/container")
async def container(token: str = Depends(oauth2_scheme)):
    # print(container)

    # container_id = container.instance_id
    container_id = token

    # create container if container_id is None
    try:
        container_info = await check_container(container_id)
    except Exception as e:
        print("New container will be created.")
    finally:
        container_info = await create_container()
        container_id = container_info["container_id"]

    # check if container exists
    container_info = await check_container(container_id)
    user_db[token] = {"container": container_info}

    print(container_info)
    return "OK"


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile, token: str = Depends(oauth2_scheme)):
    try:
        container_id = user_db[token]["container"]["container_id"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    await upload_file(container_id, file)
    return "OK"


@app.get("/downloadfile")
async def create_download_file(file_name: str, token: str = Depends(oauth2_scheme)):
    try:
        container_id = user_db[token]["container"]["container_id"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    file_response = await download_file(container_id, file_name)

    return file_response


@app.post("/run")
async def sandbox_run(code: Code, token: str = Depends(oauth2_scheme)):
    try:
        # container_port = user_db[token]["container"]["container_port"]
        container_host = user_db[token]["container"]["container_host"]
    except KeyError:
        raise HTTPException(
            status_code=500, detail="Container not found/created")

    code = jsonable_encoder(code)
    code_string = code.get("code_string")

    container_url = f"http://{container_host}:3000/run"

    data = {
        "code_string": code_string
    }

    container_response = requests.post(container_url, json=data)

    return container_response.json()

# placeholder


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    token = uuid4()

    return {"access_token": token, "token_type": "bearer"}
