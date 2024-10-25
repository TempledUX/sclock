from sclock import Clock
import pytest
import time


@pytest.fixture
def clock():
    return Clock()


def test_decorator_usage(clock: Clock):
    @clock("test_label")
    def sample_function():
        time.sleep(0.1)

    sample_function()
    times = clock.get_times("test_label")
    assert len(times) == 1
    assert times[0] > 0


def test_context_manager_usage(clock: Clock):
    with clock.using_label("context_label"):
        time.sleep(0.1)
    times = clock.get_times("context_label")
    assert len(times) == 1
    assert times[0] > 0


def test_mean_time(clock: Clock):
    @clock("mean_test_label")
    def sample_function():
        time.sleep(0.1)

    sample_function()
    sample_function()
    mean_time = clock.mean_time("mean_test_label")
    assert mean_time > 0
    assert len(clock.get_times("mean_test_label")) == 2


def test_mean_time_multiple_labels(clock: Clock):
    @clock("mean_test_label")
    def sample_function():
        time.sleep(0.1)

    @clock("mean_test_label_2")
    def sample_function2():
        time.sleep(0.3)

    sample_function()
    sample_function2()
    sample_function()
    sample_function2()
    mean_time_1 = clock.mean_time("mean_test_label")
    mean_time_2 = clock.mean_time("mean_test_label_2")
    assert mean_time_2 > mean_time_1
    assert len(clock.get_times("mean_test_label")) == 2
    assert len(clock.get_times("mean_test_label_2")) == 2