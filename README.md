# Docker Python Sandbox Supervisor

The Python Sandbox supervisor for [Code Interpreter Lite](https://github.com/uetuluk/code-interpreter-lite) project.

This supervisor will create a sandbox docker container for a request and additionally create a volume for the user.

It will handle the size and time restrictions for the container.

It can also download, upload files and run commands in the container.

## Build Image

You can build the image or pull it from Docker Hub.

```bash
make build-all-images
```

```bash
# Pull the production image
docker pull uetuluk/docker-python-sandbox-supervisor:latest

# Pull the development image
docker pull uetuluk/docker-python-sandbox-supervisor-development:latest

# Pull the worker image
docker pull uetuluk/docker-python-sandbox-supervisor-worker:latest
```

This container requires RabbitMQ to be running. You can run it with Docker Compose.

```bash
make production
```

## Development Quickstart

If you are interested in developing more features for the supervisor, you can use the development image.
Build or pull it from the Docker Hub, then run the container.

```bash
make build-development-image
make build-worker-image
```

```bash
# Pull the development image
docker pull uetuluk/docker-python-sandbox-supervisor-development:latest

# Pull the worker image
docker pull uetuluk/docker-python-sandbox-supervisor-worker:latest
```

Run the container stack.
```bash
make develop
```