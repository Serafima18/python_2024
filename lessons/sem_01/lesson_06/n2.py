from decimal import Decimal, getcontext
from contextlib import contextmanager

class Precision:
    def __init__(self, precision: float) -> None:
        if isinstance(precision, float):
            self.precision = round(precision)
        elif isinstance(precision, int):
            self.precision = precision
        else:
            raise TypeError("Precision must be an int or float.")
        if self.precision < 1:
            raise ValueError("Precision must be at least 1.")
        
        self.original_precision = getcontext().prec

    def __enter__(self) -> None:
        getcontext().prec = self.precision

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        getcontext().prec = self.original_precision