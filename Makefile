.PHONY: tests
tests:
	pytest

.PHONY: build_docker
build_docker:
	docker build . -t vault53/foapi_rest

.PHONY: push_docker
push_docker:
	docker push vault53/foapi_rest
