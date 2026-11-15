import os
from pathlib import Path
import shlex
import sys
from typing import Protocol

import plotly.graph_objects as go


def save_plot(fig: go.Figure, filepath: Path) -> None:
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
