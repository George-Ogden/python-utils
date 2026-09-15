from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self, assert_type
from unittest import mock

import pytest

from utils.test_utils import check_for_errors

from .identity import identity
from .min_max import min_max

if TYPE_CHECKING:
    from mypy_pytest_plugin_types.mock import Mock


@dataclass(frozen=True)
class WeirdCmp:
    x: int

    def __lt__(self, other: Self) -> bool:
        return (other.x - self.x) % 3 == 1


@pytest.mark.parametrize(
    "a, b, key, swap",
    [
        (3, 4, None, False),
        (4, 3, None, True),
        (3, 4, lambda x: -x, True),
        (4, 3, lambda x: -x, False),
        ("aaa", "bbb", len, False),
        ("bbb", "aaa", len, False),
        (3, 4, lambda _: 0, False),
        (4, 3, lambda _: 0, False),
    ],
)
def test_min_max(a: Any, b: Any, key: Callable[[Any], Any] | None, swap: bool) -> None:
    if swap:
        assert min_max(a, b, key=key) == (b, a)
    else:
        assert min_max(a, b, key=key) == (a, b)


@pytest.mark.parametrize(
    "it, key, expected",
    [
        ([], None, ValueError),
        (None, None, TypeError),
        ([1, 2, 3], None, (1, 3)),
        ([1, 4, 6, 8, -5, 4, 3], None, (-5, 8)),
        ([1, 4, 6, 8, 5, 4, 3], lambda x: x % 2, (4, 1)),
        ([0, 1, 2], WeirdCmp, AssertionError),
        ([5, 8, 3, 4, 1, 9], lambda x: x >= 5, (3, 5)),
        ([0], None, (0, 0)),
    ],
)
def test_min_max_iterable(
    it: Any, key: Callable[[Any], Any] | None, expected: tuple[Any, Any] | type[Exception]
) -> None:
    with check_for_errors(expected):
        assert min_max(it, key=key) == expected


@pytest.mark.typed
def test_min_max_iterable_correct_calls() -> None:
    if TYPE_CHECKING:
        m: Mock[[int], int]
    m = mock.Mock(return_value=0)
    assert min_max([5, 4, 3], key=m) == (5, 5)
    assert m.call_count == 3


@pytest.mark.typed
def test_min_max_type_hints_without_key() -> None:
    c = "abc"
    d = "def"
    assert_type(min_max(c, d), tuple[str, str])
    assert_type(min_max(c, d, key=None), tuple[str, str])
    assert_type(min_max(c, d, key=len), tuple[str, str])

    if TYPE_CHECKING:
        min_max(c, d, key=set.__len__)  # type: ignore
        min_max(c, d, key=dict.fromkeys)  # type: ignore


@pytest.mark.typed
def test_min_max_type_hints_with_key() -> None:
    a = {3: "c", 4: "d", 5: "e"}
    b = {3: "c", 4: "d"}
    assert_type(min_max(a, b, key=len), tuple[dict[int, str], dict[int, str]])

    if TYPE_CHECKING:
        min_max(a, b, key=None)  # type: ignore
        min_max(a, b)  # type: ignore
        min_max(a, b, key=identity)  # type: ignore
        min_max(a, b, len)  # type:ignore


@pytest.mark.typed
def test_min_max_iterable_type_hints_without_key() -> None:
    letters = "abracadabra"

    assert_type(min_max(letters), tuple[str, str])
    assert_type(min_max(letters, key=None), tuple[str, str])
    assert_type(min_max(letters, key=len), tuple[str, str])

    if TYPE_CHECKING:
        min_max(letters, key=set.__len__)  # type: ignore
        min_max(letters, key=dict.fromkeys)  # type: ignore


@pytest.mark.typed
def test_min_max_type_iterable_hints_with_key() -> None:
    iter = [{3: "c", 4: "d", 5: "e"}, {3: "c", 4: "d"}]
    assert_type(min_max(iter, key=len), tuple[dict[int, str], dict[int, str]])

    if TYPE_CHECKING:
        min_max(iter, key=None)  # type: ignore
        min_max(iter)  # type: ignore
        min_max(iter, key=identity)  # type: ignore
        min_max(iter, len)  # type:ignore
