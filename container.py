from docker import DockerClient
from docker.errors import DockerException
from uuid import uuid4
from fastapi import HTTPException, File
from fastapi.responses import FileResponse
import os

docker_client = DockerClient.from_env()

DOCKER_IMAGE = "docker-python-sandbox:latest"


async def create_container():
    # create a container id
    container_id = uuid4()
    try:
        # create volume
        volume = docker_client.volumes.create(name=str(container_id))

        # create container
        container = docker_client.containers.run(DOCKER_IMAGE, name=str(container_id), volumes={
            str(volume.id): {"bind": "/mnt/data", "mode": "rw"}}, ports={3000: None}, detach=True)

        container.reload()
        print(container.ports)
        container_port = container.ports['3000/tcp'][0]['HostPort']

        return {"container_id": str(container_id), "container_port": container_port}
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))


async def check_container(container_id: str):
    try:
        container = docker_client.containers.get(container_id)
        container.reload()
        container_port = container.ports['3000/tcp'][0]['HostPort']

        return {"container_id": str(container_id), "container_port": container_port}
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))


async def check_volume(container_id: str):
    try:
        container = docker_client.containers.get(container_id)
        container.reload()
        volume = container.attrs['Mounts'][0]['Name']
        return volume
    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))


async def upload_file(container_id: str, file: File):
    try:
        volume_name = await check_volume(container_id)
        print(volume_name)

        temp_file_name = f"/tmp/{file.filename}"
        with open(temp_file_name, 'wb+') as out_file:
            out_file.write(await file.read())

        docker_client.containers.run('busybox',
                                     command=f'cp "/tmp/{file.filename}" /volume',
                                     volumes={volume_name: {'bind': '/volume'},
                                              temp_file_name: {'bind': f'/tmp/{file.filename}'}},
                                     remove=True)

        os.remove(temp_file_name)

        return "OK"

    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))


async def download_file(container_id: str, file_name: str):
    try:
        volume_name = await check_volume(container_id)
        print(volume_name)

        temp_file_path = f"/tmp/{volume_name}/{file_name}"
        print(temp_file_path)

        docker_client.containers.run('busybox',
                                     command=f'cp "/volume/{file_name}" "/tmp/{volume_name}/{file_name}"',
                                     volumes={volume_name: {'bind': '/volume'},
                                              temp_file_path: {'bind': f'/tmp/{volume_name}/{file_name}', 'mode': 'rw'}},
                                     remove=True)

        # print(temp_file_path, file_name)

        response_file_path = f"/{temp_file_path}/{file_name}"

        return FileResponse(response_file_path)

    except DockerException as e:
        raise HTTPException(status_code=500, detail=str(e))
