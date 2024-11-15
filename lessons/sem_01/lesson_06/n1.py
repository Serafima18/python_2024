from functools import wraps
from typing import Callable, TypeVar, Dict

T = TypeVar("T")

def api_computable_exceptions(
    exception_mapping: Dict[type[Exception], type[Exception]]
) -> Callable[[Callable[[], T]], Callable[[], T]]:
    @wraps(exception_mapping)
    def decorator(func: Callable[[], T]) -> Callable[[], T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                # Проверяем, есть ли исключение в маппинге
                if type(exc) in exception_mapping:
                    raise exception_mapping[type(exc)]() from None
                raise  # В противном случае, возбуждаем исключение заново
        return wrapper
    return decorator

# Пример использования
class UnsupportedValueError(Exception):
    pass

class NonExistedKeyError(Exception):
    pass

exception_mapping = {
    ValueError: UnsupportedValueError,
    KeyError: NonExistedKeyError,
}

@api_computable_exceptions(exception_mapping)
def raise_value_error() -> None:
    raise ValueError

@api_computable_exceptions(exception_mapping)
def raise_key_error() -> None:
    raise KeyError

@api_computable_exceptions(exception_mapping)
def raise_exception() -> None:
    raise Exception

# Проверка
try:
    raise_value_error()
except UnsupportedValueError:
    print("Caught UnsupportedValueError")

try:
    raise_key_error()
except NonExistedKeyError:
    print("Caught NonExistedKeyError")

try:
    raise_exception()
except Exception:
    print("Caught general Exception")