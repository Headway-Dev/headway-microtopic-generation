docker_build:
	docker build --platform linux/amd64 -t hw-microtopics-update .

docker_push:
	docker tag hw-microtopics-update us-central1-docker.pkg.dev/books-us/hw-airnd/hw-microtopics-update
	docker push us-central1-docker.pkg.dev/books-us/hw-airnd/hw-microtopics-update