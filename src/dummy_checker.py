"""An example of how to implement a checker function."""

class DummyChecker:
    """An example checker class to test the student's code."""
    def __init__(self, function: callable) -> None:
        """Initialize the checker with the student's function.

        Args:
            function    : the student's function to test.
        """
        self.function = function

    def check(self, verbose: bool) -> bool:
        """An example checker function to test if the student's code returns a True.

        Args:
            verbose     : whether to print verbose output.

        Returns:
            flag        : True if the test passes, False otherwise.
        """
        if verbose:
            print("Running the checker function...")
        return self.function() == True
