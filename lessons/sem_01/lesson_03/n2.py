import time
from typing import Callable, TypeVar

T = TypeVar("T")

def collect_statistic(statistics: dict[str, list[float]]) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if func.__name__ not in statistics:
            statistics[func.__name__] = [0.0, 0]  # [time_avg, call_counter]
        
        def wrapper(*args, **kwargs) -> T:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Обновление статистики
            time_avg, call_counter = statistics[func.__name__]
            statistics[func.__name__][1] += 1
            new_avg = (time_avg * call_counter + elapsed_time) / (call_counter + 1)
            statistics[func.__name__][0] = new_avg
            
            return result

        return wrapper
    return decorator