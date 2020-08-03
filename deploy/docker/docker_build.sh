#!/usr/bin/env bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.
#
# It also relies on python 3 being present on the machine where the script
# is run from.
#
# It should be run from the root directory of nlab_core.

# Exit if any command fails
set -e

######
#nginx
######

# Create nginx.conf in the correct place
./deploy/docker/tools/create_nginx_conf.py

# Build nginx image
docker build -f deploy/docker/nginx/dockerfile \
  -t $NLAB_DOCKER_NGINX_IMAGE_NAME .

# Remove nginx.conf again
rm deploy/docker/nginx/nginx.conf

######
#mysql
######

# Build mysql image
docker build -f deploy/docker/mysql/dockerfile \
  -t $NLAB_DOCKER_MYSQL_IMAGE_NAME .

#######
#python
#######

# Create environment_variables in the correct place
./deploy/docker/tools/create_python_environment_variables.py

# Build python image
docker build -f deploy/docker/python/dockerfile \
  --build-arg NLAB_DEPLOYED_ITEX2MML_PATH \
  -t $NLAB_DOCKER_PYTHON_IMAGE_NAME .
