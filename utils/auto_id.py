import sys
from typing import ClassVar, Generic, cast

if sys.version_info >= (3, 13):
    from typing import TypeVar
else:
    from typing_extensions import TypeVar

from extra_types.types import Nat

T = TypeVar("T", default=Nat)


class AutoId(Generic[T]):
    """
    A class that has a global id that can be reset and incremented.
    It defaults to using the natural numbers (0, 1, 2, ...) but this can be overridden.
    If the type parameter is changed, the `_increment_id` and `_id_default_value` methods need to be updated.
    """

    _global_id: ClassVar[T] = cast(T, 0)

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        cls.reset_global_id()

    @classmethod
    def _increment_id(cls, id: T, /) -> T:
        """
        Transforms the current id to the next one.
        The default is to increment it.
        """
        return id + 1  # type: ignore[operator,return-value]

    @classmethod
    def next_id(cls) -> T:
        """
        Generate the next id.
        The default behavior is to increment the current id (and return the old one).
        However, this can be changed by overriding `_increment_global_id`.
        """
        id = cls._global_id
        cls._global_id = cls._increment_id(cls._global_id)
        return id

    @classmethod
    def _id_default_value(cls) -> T:
        """
        The initial and default value for the global id.
        This is set when the class is created or when `reset_global_id` is called.
        The default value is 0.
        """
        return cast(T, 0)

    @classmethod
    def reset_global_id(cls) -> None:
        """
        Reset the global id of this class to the default.
        It does not affect subclasses.
        """
        cls._global_id = cls._id_default_value()

    @classmethod
    def _reset_all_global_ids(cls) -> None:
        """
        Reset the global ids of this class and all subclasses.
        This is used by the pytest fixture to ensure all subclasses are updated.
        """
        cls.reset_global_id()
        for subclass in cls.__subclasses__():
            subclass._reset_all_global_ids()
