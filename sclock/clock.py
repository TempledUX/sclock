from collections import defaultdict
from typing import Callable
import time
import statistics


class Clock():
    def __init__(self):
        """Initializes a new Clock instance.

        The Clock instance stores timing data in an internal dictionary
        where keys are labels and values are lists of recorded time durations.
        """
        self._time_bank = defaultdict(list)

    def __call__(self, label: str) -> Callable:
        """Acts as a decorator factory to time a function.

        When an instance of Clock is called (e.g., `@clock_instance("my_label")`),
        it returns a decorator that, when applied to a function, will record
        the execution time of that function each time it's called. The recorded
        time is stored under the provided label.

        Args:
            label: The string identifier to store the recorded times under.

        Returns:
            A decorator function that can be applied to the target function.
        """
        return self._decorate_function(label)

    def _decorate_function(self, label: str) -> Callable[[Callable], Callable]:
        """Internal helper to create the actual decorator."""
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                self._time_bank[label].append(end_time - start_time)
                return result
            return wrapper
        return decorator

    def __enter__(self) -> 'Clock':
        if not hasattr(self, '_label') or self._label is None:
            raise ValueError("Label must be provided by calling 'using_label()' before entering a 'with' block.")
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Finalizes the context manager block and records the elapsed time.

        This method is called automatically when exiting a 'with' block.
        The time elapsed since `__enter__` was called is recorded under the
        label specified by a prior call to `using_label()`.

        Args:
            exc_type: The type of exception that caused the context to be exited, if any.
            exc_value: The instance of the exception, if any.
            traceback: A traceback object for the exception, if any.
        """
        end_time = time.perf_counter()
        self._time_bank[self._label].append(end_time - self._start_time)

    def using_label(self, label: str) -> 'Clock':
        """Sets the label to be used when the Clock is a context manager.

        This method must be called before entering the 'with' block
        to specify which label the timing should be associated with.

        Args:
            label: The string identifier for the timing session.

        Returns:
            The Clock instance itself, allowing for method chaining.
        """
        self._label = label
        return self

    def get_times(self, label: str) -> list[float]:
        """Retrieves all recorded time durations for a given label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            A list of floating-point numbers, where each number is a
            recorded time duration in seconds. Returns an empty list if
            the label does not exist or has no times recorded.
        """
        return self._time_bank[label]

    def mean_time(self, label: str) -> float:
        """Calculates the arithmetic mean of recorded times for a label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            The mean of the recorded times in seconds, or 0.0 if no times
            are recorded for the label.
        """
        times = self._time_bank[label]
        if not times:
            return 0.0
        return sum(times) / len(times)

    def median_time(self, label: str) -> float:
        """Calculates the median of recorded times for a given label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            The median of the recorded times in seconds, or 0.0 if no times
            are recorded for the label.
        """
        times = self._time_bank[label]
        if not times:
            return 0.0
        return statistics.median(times)

    def min_time(self, label: str) -> float:
        """Returns the minimum recorded time for a given label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            The minimum recorded time in seconds, or 0.0 if no times
            are recorded for the label.
        """
        times = self._time_bank[label]
        if not times:
            return 0.0
        return min(times)

    def max_time(self, label: str) -> float:
        """Returns the maximum recorded time for a given label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            The maximum recorded time in seconds, or 0.0 if no times
            are recorded for the label.
        """
        times = self._time_bank[label]
        if not times:
            return 0.0
        return max(times)

    def total_time(self, label: str) -> float:
        """Calculates the sum of all recorded times for a given label.

        Args:
            label: The string identifier for the set of times.

        Returns:
            The total sum of recorded times in seconds, or 0.0 if no times
            are recorded for the label.
        """
        times = self._time_bank[label]
        if not times:
            return 0.0
        return sum(times)

    def clear_times(self, label: str = None) -> None:
        """Clears recorded times.

        If a specific label is provided, only times associated with that label
        are cleared from the internal time bank. If no label is provided (i.e.,
        `label` is None), all times for all labels are cleared, effectively
        resetting the time bank.

        Args:
            label: Optional. The string identifier for the set of times to clear.
                   If None, all times for all labels are cleared.
        """
        if label is not None:
            self._time_bank.pop(label, None)  # Remove the label if it exists, otherwise do nothing.
        else:
            self._time_bank.clear()  # Clear all entries from the defaultdict.
