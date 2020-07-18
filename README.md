nlab_core
---------

This repository contains the source code for the new version of the
nLab software.

nLab deployment
---------------

To deploy the nLab locally, do the following from the root directory of
nlab-core.

source deploy/nlab_local_environment_variables
./deploy/docker/docker_build.sh
./deploy/docker/docker_run.sh

To deploy the nLab in production, do the same, but use
nlab_production_environment_variables instead.

nLab architecture
-----------------

1. All interaction with the nLab is via an nginx server.
2. The pages of the nLab are served statically by nginx, i.e. the nLab
itself is actually a static website.
