develop:
	docker compose -f docker-compose.dev.yml up

production:
	docker compose -f docker-compose.yml up

setup-docker:
	make build-all-images
	docker compose pull

build-production-image:
	docker build -t docker-python-sandbox-supervisor:latest .

build-development-image:
	docker build -t docker-python-sandbox-supervisor-development --target development .

build-worker-image:
	docker build -t docker-python-sandbox-supervisor-worker --target celery .

build-all-images:
	make build-production-image
	make build-development-image
	make build-worker-image