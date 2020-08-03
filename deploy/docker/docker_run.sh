#!/usr/bin/env bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

# Exit if any command fails
set -e

NLAB_PYTHON_ENVIRONMENT_VARIABLES_FILE_PATH=\
$(pwd)/deploy/docker/python/environment_variables
NLAB_PYTHON_SOURCE_ROOT_DIRECTORY=$(pwd)/src
NLAB_LOCAL_STATIC_ROOT_DIRECTORY=$(pwd)/deploy/nlab-static

# Setup a network for communication with the MySQL database
docker network create $NLAB_DOCKER_MYSQL_NETWORK_NAME

# Setup a network for communication with the Python backend server
docker network create $NLAB_DOCKER_BACKEND_SERVER_NETWORK_NAME

#######
#mysql
#######

# Runs mysql on its standard port (3306) with password NLAB_MYSQL_ROOT_PASSWORD
# for the 'root' user. Create a database with name NLAB_MYSQL_DATABASE_NAME.
docker run --name $NLAB_DOCKER_MYSQL_IMAGE_NAME \
  -e MYSQL_ROOT_PASSWORD=$NLAB_MYSQL_ROOT_PASSWORD \
  -e MYSQL_DATABASE=$NLAB_MYSQL_DATABASE_NAME \
  --network $NLAB_DOCKER_MYSQL_NETWORK_NAME \
  -p 3306:3306 \
  -d $NLAB_DOCKER_MYSQL_IMAGE_NAME

# Wait for MySQL to be ready
docker exec -it $NLAB_DOCKER_MYSQL_IMAGE_NAME \
  mysqladmin ping -h "127.0.0.1" \
    -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_DATABASE_PASSWORD \
    --wait=40 \
    -v

# It may be possible to remove the following eventually, it is due to some
# incompatibility between client and server versions of MySQL
docker exec -it $NLAB_DOCKER_MYSQL_IMAGE_NAME \
    mysql -u $NLAB_MYSQL_DATABASE_USER \
      -p$NLAB_MYSQL_DATABASE_PASSWORD \
      $NLAB_MYSQL_DATABASE_NAME \
      -e "\
        ALTER USER root IDENTIFIED WITH mysql_native_password BY \
       '$NLAB_MYSQL_DATABASE_PASSWORD'"

########
#python
########

# Sets up python with source directory mounted as a volume. We mount nLab pages
# pages for static viewing as a volume from NLAB_LOCAL_STATIC_ROOT_DIRECTORY
# here too, in order for python to be able to work with them.
docker run -it --name $NLAB_DOCKER_PYTHON_IMAGE_NAME \
  --env-file $NLAB_PYTHON_ENVIRONMENT_VARIABLES_FILE_PATH \
  -v $NLAB_PYTHON_SOURCE_ROOT_DIRECTORY:/usr/src/app \
  -v $NLAB_LOCAL_STATIC_ROOT_DIRECTORY:$NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY \
  -p 9000:9000 \
  -d $NLAB_DOCKER_PYTHON_IMAGE_NAME

docker network connect $NLAB_DOCKER_MYSQL_NETWORK_NAME \
  $NLAB_DOCKER_PYTHON_IMAGE_NAME
docker network connect $NLAB_DOCKER_BACKEND_SERVER_NETWORK_NAME \
  $NLAB_DOCKER_PYTHON_IMAGE_NAME

########
#nginx
#######

# Runs nginx on port NLAB_NGINX_PORT, with nLab pages for static viewing mounted
# as a volume from NLAB_LOCAL_STATIC_ROOT_DIRECTORY
docker run --name $NLAB_DOCKER_NGINX_IMAGE_NAME \
  -d -p $NLAB_NGINX_PORT:$NLAB_DEPLOYED_NGINX_PORT \
  -v $NLAB_LOCAL_STATIC_ROOT_DIRECTORY:$NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY \
  --network $NLAB_DOCKER_BACKEND_SERVER_NETWORK_NAME \
  $NLAB_DOCKER_NGINX_IMAGE_NAME

