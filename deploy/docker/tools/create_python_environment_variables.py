#!/usr/bin/python3

import os
import string

"""
This script is expected to be run from the root directory of nlab_core,
from within the docker_build.sh script
"""

def _copy_environment_variables_to_docker_directory(environment_variables):
    with open(
            "deploy/docker/python/environment_variables",
            "w") as environment_variables_file:
        environment_variables_file.write(environment_variables)

def _environment_variables():
    with open(
            "deploy/docker/tools/python_environment_variables_template",
            "r") as environment_variables_template_file:
        environment_variables_template = string.Template(
            environment_variables_template_file.read())
    return environment_variables_template.substitute(
        nlab_backend_port = os.environ["NLAB_BACKEND_PORT"],
        nlab_deployed_static_root_directory = os.environ[
            "NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY"],
        nlab_deployed_mysql_database_host = os.environ[
            "NLAB_DEPLOYED_MYSQL_DATABASE_HOST"],
        nlab_mysql_database_name = os.environ["NLAB_MYSQL_DATABASE_NAME"],
        nlab_mysql_database_password = os.environ[
            "NLAB_MYSQL_DATABASE_PASSWORD"],
        nlab_mysql_database_user = os.environ["NLAB_MYSQL_DATABASE_USER"],
        nlab_log_directory = os.environ["NLAB_DEPLOYED_LOG_DIRECTORY"])

def main():
    python_environment_variables = _environment_variables()
    _copy_environment_variables_to_docker_directory(
        python_environment_variables)

if __name__ == "__main__":
    main()
