develop:
	uvicorn main:app --reload

production:
	uvicorn main:app 

setup-docker:
	docker pull busybox