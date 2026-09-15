"""
This contains a collection of helpful pytest fixtures.
They are automatically loaded when this module is installed.
"""

from pathlib import Path
import random

import pytest

from .. import AutoId


@pytest.fixture(autouse=True, scope="session")
def setup_debug() -> None:
    """
    Setup [dbg](https://github.com/George-Ogden/dbg).
    This will put `dbg` into `builtins` so it can be used when testing without an import.
    It also sorts any unordered collections to make understanding test failures easier when using [pytest-dbg](https://github.com/George-Ogden/pytest-dbg/).
    """
    try:
        from debug import CONFIG, install
    except ImportError:
        ...
    else:
        install()
        CONFIG.sort_unordered_collections = True


@pytest.fixture
def filepath(filename: str) -> Path:
    """
    Convert a filename parameter as a string into a `Path`.
    For example:
    ```python
    import pytest
    from pathlib import Path
    @pytest.mark.parametrize(
        "filename, contents",
        [
            ("log.txt", "log_data"),
            ("scores.json", '{"player_1": 1, "player_2": 2}'),
        ]
    )
    def test_simplification(filepath: Path, contents: str) -> None:
        assert filepath.read_text() == contents
    ```
    """
    return Path(filename)


@pytest.fixture
def seed() -> int:
    return 0


@pytest.fixture(autouse=True)
def manual_seed(seed: int) -> int:
    """
    Automatically seed random generators.
    Use this by defining the seed parameter or fixture.
    In this example, each test has a different seed:
    ```python
    import pytest, random
    @pytest.mark.parametrize("seed", range(5))
    def test_random_generation(seed: int) -> None:
        result = [random.random() for _ in range(10)]
    ```
    If no seed is specified, it defaults to 0.
    This currently seeds the standard library, numpy and pytorch random libraries.
    """
    random.seed(seed)
    try:
        import numpy as np
    except ImportError:
        ...
    else:
        np.random.seed(seed)  # ruff: ignore[numpy-legacy-random]
    try:
        import torch as th  # type:ignore[import-not-found]
    except ImportError:
        ...
    else:
        th.random.manual_seed(seed)
    return seed


@pytest.fixture
def test_path(request: pytest.FixtureRequest) -> Path:
    """Returns the path of the test that is being set up."""
    return request.path


@pytest.fixture
def test_dir(test_path: Path) -> Path:
    """Returns the path of directory of the test that is being set up."""
    return test_path.parent


@pytest.fixture(autouse=True)
def reset_global_id() -> None:
    """Reset all `AutoId` subclasses between each test."""
    AutoId._reset_all_global_ids()
