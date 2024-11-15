from typing import Callable, TypeVar
import time

T = TypeVar("T")

def retry(retries: int = 3, timeout: float = 1) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries - 1:  # Don't sleep after last attempt
                        time.sleep(timeout)
            raise last_exception