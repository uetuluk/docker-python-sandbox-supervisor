from celery import Celery
from docker import DockerClient
from docker.errors import DockerException

client = DockerClient.from_env()

app = Celery('tasks', broker='pyamqp://guest@localhost:5672//')


@app.task
def remove_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.remove(force=True)
    except DockerException as e:
        print(f"Error removing container {container_id}: {str(e)}")
