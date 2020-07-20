#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

# Build nginx image
docker build -f deploy/docker/nginx/dockerfile -t $NLAB_DOCKER_NGINX_IMAGE_NAME .

# Build mysql image
docker build -f deploy/docker/mysql/dockerfile -t $NLAB_DOCKER_MYSQL_IMAGE_NAME .

# Build python image
docker build -f deploy/docker/python/dockerfile -t $NLAB_DOCKER_PYTHON_IMAGE_NAME .
