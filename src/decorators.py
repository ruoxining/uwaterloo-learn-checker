"""Utility decorators for function execution."""
import signal
from functools import wraps
from typing import Any, Callable


def timeout(seconds: int) -> Callable:
    """Create a timeout decorator for function execution.
    
    Args:
        seconds: Timeout in seconds.
    
    Returns:
        decorator: A decorator function.
    """
    def timeout_handler(signum, frame):
        raise TimeoutError("Function execution timed out")
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator
