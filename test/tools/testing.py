import difflib
import os
import subprocess
import time

def _difference_between_strings(expected, actual):
    return '\n'.join(difflib.context_diff(
        expected.split("\n"),
        actual.split("\n"),
        fromfile = 'Expected',
        tofile = 'Actual'))

def launch_backend_server():
    global backend_subprocess
    backend_subprocess = subprocess.Popen(
        [
            "docker",
            "exec",
            "-i",
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"],
            "python3",
            "backend.py"
        ],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.STDOUT)
    pid_of_backend_server_subprocess = subprocess.run(
        "docker exec -i " + \
            os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] + \
            " ps aux | grep [b]ackend.py | awk '{ print $2 }'",
        shell = True,
        capture_output = True,
        text = True)
    global pid_of_backend_server
    pid_of_backend_server = pid_of_backend_server_subprocess.stdout
    # To allow the actual server to come up
    time.sleep(1)

def shutdown_backend_server_if_running():
    if "pid_of_backend_server" in globals():
        subprocess.run(
            "docker exec -i " +
                os.environ["NLAB_DOCKER_PYTHON_IMAGE_NAME"] +
                " kill " +
                pid_of_backend_server,
            shell = True)
        del globals()["pid_of_backend_server"]
    if "backend_subprocess" in globals():
        backend_subprocess.kill()
        del globals()["backend_subprocess"]

def clean_up_static_root_directory():
    subprocess.run(
        "docker exec -it " +
            os.environ["NLAB_DOCKER_NGINX_IMAGE_NAME"] +
            " /bin/bash -c 'rm -r " +
            os.path.join(
                os.environ["NLAB_DEPLOYED_STATIC_ROOT_DIRECTORY"],
                "*") +
            "'",
        shell = True)

class TestFailedException(Exception):
    def __init__(self, test_name, message, expected, actual):
        super().__init__(
            "Test failed: " +
            test_name +
            ". " +
            message +
            "\n\n" +
            _difference_between_strings(expected, actual))
