from __future__ import annotations

from dataclasses import dataclass
from typing import cast, overload


@dataclass(eq=False, slots=True, match_args=True, init=False, repr=False)
class Box[T]:
    value: T

    @overload
    def __init__(self, value: T) -> None: ...

    @overload
    def __init__[U](self: Box[U | None]) -> None: ...

    def __init__(self, value: T | None = None) -> None:
        self.value = cast(T, value)

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value

    def is_none(self) -> bool:
        """Check whether the value is None."""
        return self.value is None

    def __bool__(self) -> bool:
        """Check whether the value is truthy."""
        return bool(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Box({self.value!r})"
