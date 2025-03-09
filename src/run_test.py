"""The code to implement your own checking function. 

The function must follow the same input and output format as the provided.
"""
from typing import ModuleType

from src.decorators import timeout
from src.dummy_checker import DummyChecker


@timeout(120)  # TODO: replace the seconds of timeout with your desired value
def run_test(module: ModuleType, verbose: bool) -> bool:
    """Write your test function here.
    
    Args:
        module      : the module to test, which should be the student's code.
        verbose     : whether to print verbose output.

    Returns:
        True if the test passes, False otherwise.
    """
    checker = DummyChecker(function=module.function) # TODO: Replace with your test code
    return checker.check(verbose=verbose)
