from __future__ import annotations

from typing import ClassVar, NamedTuple, Self, final

import more_itertools as mit
import pytest

from .test_case import test_case


@test_case
class TestCaseSample(NamedTuple):
    value: float
    should_work: bool

    @classmethod
    def positive_value(cls) -> Self:
        return cls(1.0, True)

    @classmethod
    def negative_value(cls) -> Self:
        return cls(-1.0, True)

    @classmethod
    def _invalid_value(cls) -> Self:
        return cls(float("nan"), False)


TestCaseSample.__test__ = False  # type: ignore[attr-defined]


@pytest.mark.parametrize("case", TestCaseSample.cases())
def test_test_case_sample_cases(case: TestCaseSample) -> None:
    assert isinstance(case, TestCaseSample)
    assert case.should_work


def test_test_case_sample_length() -> None:
    assert len(TestCaseSample.cases()) == 2
    assert mit.all_unique(TestCaseSample.cases())  # type: ignore[iterable-sequence]


@test_case
class SomeNumbersTestCase(NamedTuple):
    x: int
    y: int | None = None

    @classmethod
    def just_x(cls) -> Self:
        return cls(3)

    @classmethod
    def x_and_y(cls) -> Self:
        return cls(4, 5)


@pytest.mark.typed
def test_cases_normal_names() -> None:

    params = SomeNumbersTestCase.cases()
    assert params == [
        pytest.param(SomeNumbersTestCase(3), id="just_x"),
        pytest.param(SomeNumbersTestCase(4, 5), id="x_and_y"),
    ]


@pytest.mark.parametrize("case", SomeNumbersTestCase.cases())
def test_some_numbers_test_case(case: SomeNumbersTestCase) -> None:
    assert isinstance(case, SomeNumbersTestCase)
    (x, y) = case
    assert isinstance(x, int)
    assert isinstance(y, int | None)


@final
@test_case
class StringTestCase(NamedTuple):
    s: str

    @classmethod
    def good_string(cls) -> Self:
        return cls("good")

    @classmethod
    def bad_string_xfail(cls) -> StringTestCase:
        return cls("bad")

    @classmethod
    def _not_a_test_case(cls) -> Self:
        return cls("sad")


@pytest.mark.typed
def test_cases_changed_names() -> None:
    params = StringTestCase.cases()
    assert params == [
        pytest.param(
            StringTestCase("bad"), id="bad_string_xfail", marks=pytest.mark.xfail(strict=True)
        ),
        pytest.param(StringTestCase("good"), id="good_string"),
    ]


@pytest.mark.parametrize("case", StringTestCase.cases())
def test_string_test_case(case: StringTestCase) -> None:
    assert isinstance(case, StringTestCase)
    (s,) = case
    assert s == "good"


@test_case
class BoolTestCase(NamedTuple):
    a: bool
    c: ClassVar[str] = "classy"  # type: ignore[valid-type]

    def inner_method(self) -> Self:
        return type(self)(False)

    @property
    def property(self) -> Self:
        return type(self)(False)

    @staticmethod
    def staticmethod() -> BoolTestCase:
        return BoolTestCase(False)

    @classmethod
    def correct(cls) -> BoolTestCase:
        return cls(True)

    @classmethod
    def wrong_type_xfail(cls) -> None:  # type: ignore[test-case]
        # Keep type ignore comment to ensure Mypy plugin detects error.
        ...


@pytest.mark.typed
def test_cases_extra_objects() -> None:
    params = BoolTestCase.cases()
    assert params == [
        pytest.param(BoolTestCase(True), id="correct"),
        pytest.param(None, id="wrong_type_xfail", marks=pytest.mark.xfail(strict=True)),
    ]


@pytest.mark.parametrize("case", BoolTestCase.cases())
def test_bool_test_case(case: BoolTestCase) -> None:
    assert case.a


@test_case
class CasesOverride(NamedTuple):
    @classmethod
    def cases(cls) -> list[int]:
        return [1, 2, 3, 4, 5]


@pytest.mark.typed
def test_cases_overridden() -> None:
    params = CasesOverride.cases()
    assert params == list(range(1, 6))


@pytest.mark.parametrize("case", CasesOverride.cases())
def test_override_test_case(case: int) -> None:
    assert case in list(range(1, 6))
