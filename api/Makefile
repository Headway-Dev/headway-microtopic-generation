docker_build:
	docker build -t hw-airnd-book-topics --platform linux/amd64 .

docker_push:
	docker tag hw-airnd-book-topics us-central1-docker.pkg.dev/books-us/hw-airnd/hw-airnd-book-topics
	docker push us-central1-docker.pkg.dev/books-us/hw-airnd/hw-airnd-book-topics