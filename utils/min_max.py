from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any, overload

from extra_types.types import Unmodified
from typing_extensions import sentinel

from .identity import identity

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT

_MISSING = sentinel("_MISSING")


@overload
def min_max[T: SupportsDunderLT](
    a: T, b: T, /, *, key: None = None
) -> tuple[Unmodified[T], Unmodified[T]]: ...
@overload
def min_max[T, U: SupportsDunderLT](
    a: T, b: T, /, *, key: Callable[[T], U]
) -> tuple[Unmodified[T], Unmodified[T]]: ...
@overload
def min_max[T: SupportsDunderLT](
    iter: Iterable[T], /, *, key: None = None
) -> tuple[Unmodified[T], Unmodified[T]]: ...
@overload
def min_max[T, U: SupportsDunderLT](
    iter: Iterable[T], /, *, key: Callable[[T], U]
) -> tuple[Unmodified[T], Unmodified[T]]: ...


def min_max(
    a: Any, b: Any = _MISSING, /, *, key: Callable[[Any], Any] | None = None
) -> tuple[Any, Any]:
    """
    Return the min and the max of two items as a tuple.
    The first item in the min and the second is the max.
    It is also possible to specify a key which is used for comparison.
    In the case of a tie, the original order is maintained.
    For example:
    ```python
    >>> from utils import min_max
    >>> min_max(0, 5)
    (0, 5)
    >>> min_max(0.5, 0.1)
    (0.1, 0.5)
    >>> import operator
    >>> min_max(10, 5, key=operator.neg)  # compare by lambda x: -x
    (10, 5)
    >>> min_max("gfed", "cba", key=lambda _: 0)
    ('cfed', 'cba')
    ```
    """
    if b is _MISSING:
        return _min_max_iterable(a, key=key)
    return _min_max_pair(a, b, key=key)


def _min_max_pair(a: Any, b: Any, /, *, key: Callable[[Any], Any] | None) -> Any:
    if key is None:
        key = identity
    if key(b) < key(a):
        return b, a
    return a, b


def _min_max_iterable(iterable: Iterable[Any], /, *, key: Callable[[Any], Any] | None) -> Any:
    if key is None:
        key = identity
    iterator = iter(iterable)
    try:
        first_item = next(iterator)
    except StopIteration as e:
        raise ValueError("Cannot find min/max of an empty iterable.") from e
    min = max = first_item
    min_key = max_key = key(first_item)
    for item in iterator:
        item_key = key(item)
        if item_key < min_key:
            min = item
            min_key = item_key
        elif max_key < item_key:
            max = item
            max_key = item_key
    return min, max
