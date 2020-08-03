#!/usr/bin/python3

import os
import string

"""
This script is expected to be run from the root directory of nlab_core,
from within the docker_build.sh script
"""

def _copy_nginx_config_to_docker_directory(nginx_config):
    with open("deploy/docker/nginx/nginx.conf", "w") as nginx_config_file:
        nginx_config_file.write(nginx_config)

def _nginx_config():
    with open(
            "deploy/docker/tools/nginx_template.conf",
            "r") as nginx_config_template_file:
        nginx_config_template = string.Template(
            nginx_config_template_file.read())
    return nginx_config_template.substitute(
        nlab_backend_port = os.environ["NLAB_BACKEND_PORT"],
        nlab_deployed_nginx_port = os.environ["NLAB_DEPLOYED_NGINX_PORT"],
        nlab_deployed_static_root_directory = os.environ[
            "NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY"])

def main():
    nginx_config = _nginx_config()
    _copy_nginx_config_to_docker_directory(nginx_config)

if __name__ == "__main__":
    main()
