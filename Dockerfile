FROM python:3.10.12 as base

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN --mount=type=cache,target=/root/.cache \ 
    pip install -r /tmp/requirements.txt

COPY . /app

FROM base as celery
CMD ["celery", "-A", "celery_worker.app", "worker", "--loglevel=info"]

FROM base as development

EXPOSE 3000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]

FROM base as default
EXPOSE 3000

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "3000"]