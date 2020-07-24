nLab code testing
------------------

Always use a clean docker setup for running tests, i.e. run

```bash
deploy/docker/docker_stop_and_remove.sh
```

(if necessary) and then the following.

```bash
deploy/docker/docker_run.sh
```

Change directory to test (all tests must be run from this location).

```bash
cd test
```

Then either run

```bash
populate_database_with_test_data.sh
```

or, the first time you wish to run the tests, use the flag `-p`, or its
longer form `--populate-database`, as follows.

```bash
page_renderer_test.py -p
```

After this, if you wish to run the tests again, simply run

```bash
page_renderer_test.py
```

without populating the database with test data again.

If all tests pass, you will receive the output `All tests passed` upon running
the above script. Otherwise, you will receive as output the details of which
test failed, and what exactly failed.
