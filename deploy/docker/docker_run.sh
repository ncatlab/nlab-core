#!/usr/bin/env bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

NLAB_PYTHON_ENVIRONMENT_VARIABLES_FILE_PATH=\
$(pwd)/deploy/docker/python/environment_variables
NLAB_PYTHON_SOURCE_ROOT_DIRECTORY=$(pwd)/src
NLAB_STATIC_ROOT_DIRECTORY=$(pwd)/deploy/nlab-static

# Setup a network for communication with the MySQL database
docker network create $NLAB_DOCKER_MYSQL_NETWORK_NAME

# Runs nginx on port NLAB_NGINX_PORT, with nLab pages for static viewing mounted
# as a volume from NLAB_STATIC_ROOT_DIRECTORY
docker run --name $NLAB_DOCKER_NGINX_IMAGE_NAME \
  -d -p $NLAB_NGINX_PORT:80 \
  -v $NLAB_STATIC_ROOT_DIRECTORY:/usr/share/nginx/html/nlab \
  $NLAB_DOCKER_NGINX_IMAGE_NAME

# Runs mysql on its standard port (3306) with password NLAB_MYSQL_ROOT_PASSWORD
# for the 'root' user. Create a database with name NLAB_MYSQL_DATABASE_NAME.
docker run --name $NLAB_DOCKER_MYSQL_IMAGE_NAME \
  -e MYSQL_ROOT_PASSWORD=$NLAB_MYSQL_ROOT_PASSWORD \
  -e MYSQL_DATABASE=$NLAB_MYSQL_DATABASE_NAME \
  --network $NLAB_DOCKER_MYSQL_NETWORK_NAME \
  -p 3306:3306 \
  -d $NLAB_DOCKER_MYSQL_IMAGE_NAME

# Sets up python with source directory mounted as a volume
docker run -it --name $NLAB_DOCKER_PYTHON_IMAGE_NAME \
  --env-file $NLAB_PYTHON_ENVIRONMENT_VARIABLES_FILE_PATH \
  --network $NLAB_DOCKER_MYSQL_NETWORK_NAME \
  -v $NLAB_PYTHON_SOURCE_ROOT_DIRECTORY:/usr/src/app \
  -d $NLAB_DOCKER_PYTHON_IMAGE_NAME
