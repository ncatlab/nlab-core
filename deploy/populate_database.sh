#!/usr/bin/env bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

# Imports the mysql file specified in NLAB_DOCKER_SQL_FILE_PATH into the
# docker MySQL database with name NLAB_MYSQL_DATABASE_NAME.
cat $NLAB_DOCKER_SQL_FILE_PATH | \
docker exec -i $NLAB_DOCKER_MYSQL_IMAGE_NAME \
  mysql -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_ROOT_PASSWORD \
    $NLAB_MYSQL_DATABASE_NAME
