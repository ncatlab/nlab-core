#!/usr/bin/env bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

#Stop and remove the nginx container
docker stop $NLAB_DOCKER_NGINX_IMAGE_NAME
docker rm $NLAB_DOCKER_NGINX_IMAGE_NAME

#Stop and remove the mysql container
docker stop $NLAB_DOCKER_MYSQL_IMAGE_NAME
docker rm $NLAB_DOCKER_MYSQL_IMAGE_NAME

#Stop and remove the python container
docker stop $NLAB_DOCKER_PYTHON_IMAGE_NAME
docker rm $NLAB_DOCKER_PYTHON_IMAGE_NAME

# Disconnect from the network NLAB_DOCKER_MYSQL_NETWORK_NAME, and remove it
docker network rm $NLAB_DOCKER_MYSQL_NETWORK_NAME

# Disconnect from the network NLAB_DOCKER_BACKEND_SERVER_NETWORK_NAME, and
# remove it
docker network rm $NLAB_DOCKER_BACKEND_SERVER_NETWORK_NAME
