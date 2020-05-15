all:

build:
	DOCKER_BUILDKIT=1 docker build -t proelbtn/codimd-exporter .
