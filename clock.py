from collections import defaultdict
from typing import Callable
import time


class Clock():
    def __init__(self):
        self._time_bank = defaultdict(list)

    def __call__(self, label: str):
        return self._decorate_function(label)

    def _decorate_function(self, label: str):
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                self._time_bank[label].append(end_time - start_time)
                return result
            return wrapper
        return decorator

    def __enter__(self):
        if not hasattr(self, '_label') or self._label is None:
            raise ValueError("Label must be provided when using Clock as a context manager.")
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.perf_counter()
        self._time_bank[self._label].append(end_time - self._start_time)

    def using_label(self, label: str):
        self._label = label
        return self

    def get_times(self, label: str):
        return self._time_bank[label]

    def mean_time(self, label: str):
        times = self._time_bank[label]
        return sum(times) / len(times)
