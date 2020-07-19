#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

# Imports the mysql file specified in NLAB_DOCKER_SQL_FILE_PATH into the
# docker MySQL database with name NLAB_MYSQL_DATABASE_NAME.
cat $NLAB_DOCKER_SQL_FILE_PATH | \
mysql -h '0.0.0.0' \
  -P '3306' \
  -u 'root' \
  -p$NLAB_MYSQL_ROOT_PASSWORD \
  $NLAB_MYSQL_DATABASE_NAME
