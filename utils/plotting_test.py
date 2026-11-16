from pathlib import Path
from typing import Literal
from unittest import mock

import plotly.graph_objects as go
import pytest

from .plotting import save_or_preview


@pytest.mark.typed
def test_save_or_preview_no_kwargs() -> None:
    @save_or_preview  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    def fake_plot() -> Literal[0]:
        return 0

    assert fake_plot() == 0
    assert fake_plot(filepath=None) == 0
    assert fake_plot(preview=False) == 0
    assert fake_plot(filepath=None, preview=False) == 0
    assert fake_plot(preview=False, filepath=None) == 0


@pytest.mark.typed
def test_save_or_preview_to_file(tmp_path: Path) -> None:
    @save_or_preview
    def empty_plot() -> go.Figure:
        return go.Figure(go.Scatter())

    filepath = tmp_path / "plot1.pdf"

    assert not filepath.exists()
    fig = empty_plot()
    assert not filepath.exists()
    assert isinstance(fig, go.Figure)

    filepath = tmp_path / "plot2.pdf"

    assert not filepath.exists()
    fig = empty_plot(filepath=filepath)
    assert filepath.exists()
    assert isinstance(fig, go.Figure)

    filepath = tmp_path / "plot3.pdf"

    assert not filepath.exists()
    fig = empty_plot(preview=False, filepath=filepath)
    assert filepath.exists()
    assert isinstance(fig, go.Figure)


@pytest.mark.typed
def test_save_or_preview_show() -> None:
    @save_or_preview
    def mock_plot() -> go.Figure:
        return mock.Mock()  # type: ignore[return-value]

    fig = mock_plot()
    fig.show.assert_not_called()  # type: ignore[attr-defined]  # ty: ignore[missing-attribute]

    fig = mock_plot(preview=True)
    fig.show.assert_called_once()  # type: ignore[attr-defined]  # ty: ignore[missing-attribute]

    fig = mock_plot(filepath=None, preview=True)
    fig.show.assert_called_once()  # type: ignore[attr-defined]  # ty: ignore[missing-attribute]
