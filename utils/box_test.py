import pytest
from pytest import Subtests

from .box import Box


@pytest.fixture
def box[T](value: T) -> Box[T]:
    return Box(value)


@pytest.mark.parametrize(
    "type_, display",
    [
        (Box, "<class 'utils.box.Box'>"),
        (Box[int], "utils.box.Box[int]"),
        (Box[Box[int]], "utils.box.Box[utils.box.Box[int]]"),
    ],
)
def test_box_type_display(type_: type[Box], display: str) -> None:
    assert str(type_) == repr(type_) == display


@pytest.mark.typed
def test_box_mutability() -> None:
    box = Box(3)
    # here for type checking
    box.value + 1
    assert box.value == 3
    box.value = 5
    assert box.value == 5

    # type check (do not delete comment)
    box.value = 3.5  # type: ignore [assignment]  # ty:ignore[invalid-assignment]


@pytest.mark.parametrize(
    "value, is_none, truth",
    [
        # empty
        (None, True, False),
        # truthy
        (1, False, True),
        # falsy
        (0, False, False),
    ],
)
def test_box_empty_and_bool(box: Box, is_none: bool, truth: bool, subtests: Subtests) -> None:
    with subtests.test("is_none"):
        assert box.is_none() is is_none
    with subtests.test("__bool__"):
        assert bool(box) is truth
