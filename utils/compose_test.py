# ruff: file-ignore[unnecessary-lambda]
from . import compose

# Note: some of these tests are written with explicit functions due to Mypy errors.


def test_compose_one_arg() -> None:
    assert compose(lambda r: list(r), range)(3) == [0, 1, 2]


def test_compose_no_args() -> None:
    assert compose(range, lambda: 10)() == range(10)


def test_compose_multiple_args() -> None:
    assert compose(tuple, lambda start, stop, step: range(start, stop, step))(0, 10, 2) == (
        0,
        2,
        4,
        6,
        8,
    )


def test_compose_kwargs() -> None:
    assert compose(lambda squares: set(squares), enumerate)(start=1, iterable=[1, 4, 9]) == {
        (1, 1),
        (2, 4),
        (3, 9),
    }
