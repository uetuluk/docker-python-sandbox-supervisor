develop:
	uvicorn main:app --reload

production:
	uvicorn main:app 

setup-docker:
	docker pull busybox

run-celery:
	docker compose up -d
	celery -A celery_worker.app worker --loglevel=info