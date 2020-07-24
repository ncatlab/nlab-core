#!/usr/bin/bash

# This script relies on the environment variables in one of
#
# nlab_production_environment_variables
# nlab_local_environment_variables
#
# being set.

# It may be possible to remove the following eventually, it is due to some
# incompatibility between client and server versions of MySQL
mysql -h $NLAB_MYSQL_DATABASE_HOST -u $NLAB_MYSQL_DATABASE_USER \
    -p$NLAB_MYSQL_DATABASE_PASSWORD $NLAB_MYSQL_DATABASE_NAME -e "\
    ALTER USER root IDENTIFIED WITH mysql_native_password BY \
    '$NLAB_MYSQL_DATABASE_PASSWORD'"

# Imports the mysql file specified in NLAB_DOCKER_SQL_FILE_PATH into the
# docker MySQL database with name NLAB_MYSQL_DATABASE_NAME.
cat $NLAB_DOCKER_SQL_FILE_PATH | \
mysql -h $NLAB_MYSQL_DATABASE_HOST \
  -u $NLAB_MYSQL_DATABASE_USER \
  -p$NLAB_MYSQL_ROOT_PASSWORD \
  $NLAB_MYSQL_DATABASE_NAME
