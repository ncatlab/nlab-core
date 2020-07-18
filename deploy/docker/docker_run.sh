#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

NLAB_STATIC_ROOT_DIRECTORY=$(pwd)/deploy/nlab-static

# Runs nginx on port NLAB_NGINX_PORT
docker run --name $NLAB_DOCKER_NGINX_IMAGE_NAME \
  -d -p $NLAB_NGINX_PORT:80 \
  -v $NLAB_STATIC_ROOT_DIRECTORY:/usr/share/nginx/html/nlab \
  $NLAB_DOCKER_NGINX_IMAGE_NAME
