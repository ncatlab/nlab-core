import difflib

def _difference_between_strings(expected, actual):
    return '\n'.join(difflib.context_diff(
        expected.split("\n"),
        actual.split("\n"),
        fromfile = 'Expected',
        tofile = 'Actual'))

class TestFailedException(Exception):
    def __init__(self, test_name, message, expected, actual):
        super().__init__(
            "Test failed: " +
            test_name +
            ". " +
            message +
            "\n\n" +
            _difference_between_strings(expected, actual))
