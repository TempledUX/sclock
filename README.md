# Simple Clock (sclock)

[![PyPI version](https://img.shields.io/pypi/v/sclock?color=blue)](https://pypi.org/project/sclock/)

Easy to use clock class, written in vanilla python. Allows to benchmark python code withing a function or with block. Contains multiple time banks for benchmarking different functions or with blocks independently.

## Examples
**Measuring code in a function as a decorator:**
```python
from sclock import Clock
clock = Clock()

@clock("custom_label")
def example_function():
    time.sleep(1)

example_function()
print(clock.get_times("custom_label"))
print(clock.mean_time("custom_label"))
```
**Measuring code in a with block:**
```python
from sclock import Clock
clock = Clock()

with clock.using_label("with_code"):
    time.sleep(2)

print(clock.get_times("with_code"))
print(clock.mean_time("with_code"))
```
