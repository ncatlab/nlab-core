nLab code testing
=================

When it is important that the tests all pass, e.g. when merging new code to
master, always use a clean docker setup for running tests, i.e. run

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
all_tests.py -p
```

After this, if you wish to run the tests again, simply run

```bash
all_tests.py
```

without populating the database with test data again.

If all tests pass, you will receive the output `All tests passed` upon running
the above script. Otherwise, you will receive as output the details of which
test failed, and what exactly failed.

The tests for a particular python module can be run individually. For example,
to test `page_renderer.py`, one can run the following. The flag
`-p/--populate-database` can be used in the same way in these cases.

```bash
page_renderer_test.py
```

Notes
-----

Many of the tests make liberal use of the option

```python
shell = True
```

when using the Python `subprocess.run` function. This is fine in the intended
context, but care should be taken if the code is borrowed and run in other
contexts.
