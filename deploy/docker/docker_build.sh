#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

#Build nginx image
echo "$NLAB_DOCKER_NGINX_IMAGE_NAME"
docker build -f deploy/docker/nginx/dockerfile -t $NLAB_DOCKER_NGINX_IMAGE_NAME .

#Build mysql image
echo "$NLAB_DOCKER_MYSQL_IMAGE_NAME"
docker build -f deploy/docker/mysql/dockerfile -t $NLAB_DOCKER_MYSQL_IMAGE_NAME .
