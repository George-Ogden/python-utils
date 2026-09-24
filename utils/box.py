from __future__ import annotations

from dataclasses import dataclass
from typing import cast, overload


@dataclass(eq=False, slots=True, match_args=True, init=False, repr=False)
class Box[T]:
    """
    Wrap a value in a `Box`.
    The main use cases of the `Box` are interior mutability and passing values by reference.
    `Box`es are unique by their `id` so `Box(3) != Box(3)`, but `box = Box(3); box == box`.
    The box has multiple pass through methods to act on the underlying data.
    """

    value: T

    @overload
    def __init__(self, value: T) -> None:
        """Initialize a `Box` with a value."""

    @overload
    def __init__[U](self: Box[U | None]) -> None:
        """Initialize a `Box` with a default value of `None`."""

    def __init__(self, value: T | None = None) -> None:
        self.value = cast(T, value)

    def get(self) -> T:
        """Read the value."""
        return self.value

    def set(self, value: T) -> None:
        """Update the value."""
        self.value = value

    def is_none(self) -> bool:
        """Check whether the value is `None`."""
        return self.value is None

    def __bool__(self) -> bool:
        """Check whether the value is truthy."""
        return bool(self.value)

    def __str__(self) -> str:
        """Represent the value in the box."""
        return str(self.value)

    def __repr__(self) -> str:
        return f"Box({self.value!r})"
