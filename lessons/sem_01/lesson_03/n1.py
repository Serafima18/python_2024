from typing import Callable

def make_averager(accumulation_period: int) -> Callable[[float], float]:
    values = []

    def get_avg(income: float) -> float:
        nonlocal values
        
        values.append(income)
        
        # Если количество наблюдений меньше периода, берем среднее по всем наблюдениям
        if len(values) < accumulation_period:
            return sum(values) / len(values)
        
        # Иначе берем среднее по последним accumulation_period наблюдениям
        return sum(values[-accumulation_period:]) / accumulation_period

    return get_avg