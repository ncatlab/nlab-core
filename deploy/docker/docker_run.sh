#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

NLAB_STATIC_ROOT_DIRECTORY=$(pwd)/deploy/nlab-static

# Runs nginx on port NLAB_NGINX_PORT, with nLab pages for static viewing mounted
# as a volume from NLAB_STATIC_ROOT_DIRECTORY
docker run --name $NLAB_DOCKER_NGINX_IMAGE_NAME \
  -d -p $NLAB_NGINX_PORT:80 \
  -v $NLAB_STATIC_ROOT_DIRECTORY:/usr/share/nginx/html/nlab \
  $NLAB_DOCKER_NGINX_IMAGE_NAME

# Runs mysql on its standard port (3306) with password NLAB_MYSQL_ROOT_PASSWORD
# for the 'root' user.
docker run --name $NLAB_DOCKER_MYSQL_IMAGE_NAME \
  -e MYSQL_ROOT_PASSWORD=$NLAB_MYSQL_ROOT_PASSWORD \
  -e MYSQL_DATABASE=$NLAB_MYSQL_DATABASE_NAME \
  -p 3306:3306 \
  -d $NLAB_DOCKER_MYSQL_IMAGE_NAME
