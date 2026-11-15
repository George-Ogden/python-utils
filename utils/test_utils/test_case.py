from __future__ import annotations

import inspect
import typing
from typing import TYPE_CHECKING, Protocol, Self, final

import pytest

if TYPE_CHECKING:
    from mypy_pytest_plugin_types import ParameterSet
    from ty_extensions import Intersection  # type: ignore[import-not-found]


def _marks_for(name: str) -> tuple[()] | pytest.MarkDecorator:
    if name.endswith("xfail"):
        return pytest.mark.xfail(strict=True)
    return ()


def _cases[Self: type](cls: Self) -> list[ParameterSet[Self]]:
    return [  # ty: ignore[invalid-explicit-return]
        pytest.param(method(), id=name, marks=_marks_for(name))
        for name, method in inspect.getmembers(cls, predicate=inspect.ismethod)
        if name != "cases" and not name.startswith("_")
    ]


class CasesAware(Protocol):
    def cases(self) -> list[ParameterSet[Self]]:
        raise NotImplementedError()


@pytest.mark.typed
@typing.no_type_check
def test_case[T: type](cls: T) -> Intersection[T, CasesAware]:
    """
    The `@test_case` decorator is experimental and under development.
    It adds a `cases` `classmethod`, which returns an iterable that called every other `classmethod` that didn't start with an underscore.
    Here's an example:
    ```python
    import pytest

    from utils.test_utils import test_case
    from typing import NamedTuple, Self

    @test_case
    class CustomTestCase(NamedTuple):
        positive: float
        negative: float

        @classmethod
        def one_test_case(cls) -> Self:
            return cls(1.0, -1.0)

        @classmethod
        def zero_test_case(cls) -> Self:
            return cls(
                cls._utility_function_to_return_zero(),
                cls._utility_function_to_return_zero()
            )

        @classmethod
        def _utility_function_to_return_zero(cls) -> float:
            \"\"\"This method is not used as a test case because it starts with an underscore.\"\"\"
            return 0.0

        def pseudo_negation(self) -> float:
            \"\"\"This method is not used as a test case because it is an instance method.\"\"\"
            return -self.positive

    @pytest.mark.parametrize("case", CustomTestCase.cases())
    def test_negation(case: CustomTestCase) -> None:
        assert -case.positive == case.negative
        assert case.pseudo_negation() == case.negative
    ```
    This expands to two tests: `test_negation[zero_test_case]` and `test_negation[one_test_case]`.
    They both pass.

    This cannot be typed well in the Python type system (yet), so there is a mypy plugin.
    This plugin relies on the [`mypy_pytest_plugin`](https://github.com/George-Ogden/mypy-pytest).
    The plugin assumes that each method returns the original class (`Self`).

    Add it to your `mypy.ini` like this:
    ```ini
    [mypy]
    plugins = mypy_pytest_plugin, utils.plugins.mypy_plugin
    ```
    """
    if not hasattr(cls, "cases"):
        cls.cases = classmethod(_cases)
    return final(cls)


test_case.__test__ = False  # ty: ignore[missing-attribute]
