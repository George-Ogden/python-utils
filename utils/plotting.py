"""
Plotting utilities.

These is enabled with the `plotting` extra:
```bash
pip install 'utils[extra]'
```
"""

import os
from pathlib import Path
import shlex
import sys
from typing import Protocol

import plotly.graph_objects as go


def save_plot(fig: go.Figure, filepath: Path) -> None:
    """
    Save a plot to a file as a PDF.
    This prints the quoted filename (using `shlex.quote`) when saved.
    """
    fig.write_image(file=filepath, height=1080, width=1920, format="pdf")
    print(shlex.quote(os.fspath(filepath)), file=sys.stderr)


class AutoSaveInputProtocol[**P](Protocol):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> go.Figure:
        raise NotImplementedError()


class AutoSaveOutputProtocol[**P](Protocol):
    def __call__(  # type: ignore[valid-type]
        self,
        *args: P.args,
        filepath: Path | None = None,  # ty: ignore[invalid-paramspec]
        preview: bool = False,
        **kwargs: P.kwargs,
    ) -> go.Figure:
        raise NotImplementedError()


def autosave[**P](fn: AutoSaveInputProtocol[P]) -> AutoSaveOutputProtocol[P]:
    """
    Wrap a function that generates a `go.Figure` with saving options.

    The options are `preview`, which will call `fig.show()`,
    and `filepath` which will save the plot to the filepath using `save_plot`.
    They are both optional.
    `preview` defaults to `False` and `filepath` defaults to `None`.
    """

    def inner(  # type: ignore[valid-type]
        *args: P.args,
        filepath: Path | None = None,  # ty: ignore[invalid-paramspec]
        preview: bool = False,
        **kwargs: P.kwargs,
    ) -> go.Figure:
        fig = fn(*args, **kwargs)
        if preview:
            fig.show()
        if filepath is not None:
            save_plot(fig, filepath)
        return fig

    return inner
