nlab_core
---------

This repository contains the source code for the new version of the
nLab software.

nLab deployment
---------------

To deploy the nLab locally, do the following from the root directory of
nlab-core.

```bash
source deploy/nlab_local_environment_variables
./deploy/docker/docker_build.sh
./deploy/docker/docker_run.sh
```

This creates an nLab installation with an empty database with name set to the
value of the environment variable `NLAB_MYSQL_DATABASE_NAME`. To populate that
database from an SQL dump, wait a minute or two to give the MySQL database time
to come up, then set the environment variable `NLAB_DOCKER_SQL_FILE_PATH` in
`deploy/local_environment_variables` to the absolute file path of the SQL dump,
run

```bash
source deploy/nlab_local_environment_variables
```

again, and run the following in addition.

```bash
./deploy/populate_database.sh
```

To deploy the nLab in production, follow all of these steps in the same way, but
use `nlab_production_environment_variables` instead.

The nginx docker image uses an `nginx.conf` file which is created by the
following script.

```bash
./deploy/docker/tools/create_nginx_conf.py
```

It replaces the placeholders in the template `nginx_template.conf` with
environment variables of the same name in
`deploy/nlab_local_environment_variables` or
`deploy/nlab_production_environment_variables`.

Similarly, the python docker image uses an `environment_variables` file which is
created by the following script.

```bash
./deploy/docker/tools/create_python_environment_variables.py
```

It replaces the placeholders in the template `python_environment_variables` with
environment variables of the same name in
`deploy/nlab_local_environment_variables` or
`deploy/nlab_production_environment_variables`.

In both cases, changing the value of one of the placeholders should be achieved
by changing `deploy/nlab_local_environment_variables` and/or
`deploy/nlab_production_environment_variables`, and re-building (this is not
necessary for the python docker image) and re-running the docker image.

Tweaking the nginx config in such a way that a new environment variable is
needed should be achieved by tweaking both `nginx_template.conf` and
`deploy/docker/tools/create_nginx_conf.py`, and then proceeding as in the
previous paragraph. Similarly for adding a new python environment variable.

nLab architecture
-----------------

1. All interaction with the nLab is via an nginx server.
2. The pages of the nLab are served statically by nginx, i.e. the nLab
itself is actually a static website.
3. The nLab is backed by a MySQL database which stores, for a given page,
metadata about this page, and the markdown source.
4. There is a backend application server (CherryPy), which nginx
(reverse) proxies to in some cases.
5. The static pages served by nginx are generated from the database in one of
the following ways: i) upon page edit ii) by a GET call to the backend
server iii) manually. All of these rely on the functions in
`render_nlab_page_for_viewing.py`, which in turn rely on `page_renderer.py`
and `source_renderer.py`.

nLab code testing
-----------------

Before pushing/merging to master, all tests must pass. The tests must be run
manually. See the README.md file in test/ for details on how to run the tests.
