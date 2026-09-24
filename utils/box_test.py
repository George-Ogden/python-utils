import pytest
from pytest import Subtests

from . import Box, unreachable


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


@pytest.mark.typed
def test_box_equality() -> None:
    left = Box(10)
    right = Box(10)
    assert left == left is left  # ruff: ignore[comparison-with-itself]
    assert right == right is right  # ruff: ignore[comparison-with-itself]
    assert left != right is not left
    assert right != left is not right


@pytest.mark.typed
def test_box_pattern_mtach() -> None:
    nested_box = Box(Box(3))
    match nested_box:
        case Box(_):
            ...
        case _:
            unreachable()

    match nested_box:
        case Box(Box(_)):
            ...
        case _:
            unreachable()

    match nested_box:
        case Box(Box(2)):
            unreachable()
        case Box(Box(3)):
            ...
        case _:
            unreachable()


@pytest.mark.parametrize(
    "box, display, debug",
    [
        (Box(), "None", "Box(None)"),
        (Box(Box(3)), "3", "Box(Box(3))"),
        (Box("text"), "text", "Box('text')"),
    ],
)
def test_box_display(box: Box, display: str, debug: str) -> None:
    assert str(box) == display
    assert repr(box) == debug


@pytest.mark.parametrize("inner", [[], (), 10, True, None])
def test_box_hash[T](inner: T) -> None:
    left = Box(inner)
    right = Box(inner)
    try:
        inner_hash = hash(inner)
    except TypeError:
        inner_hash = -1
    assert hash(left) == hash(left) != inner_hash
    assert hash(right) == hash(right) != inner_hash
    assert hash(left) != hash(right)
