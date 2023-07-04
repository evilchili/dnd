import os
from configparser import ConfigParser
from pathlib import Path
from textwrap import dedent
from typing import List, Union

import rich.repr
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.styles import Style
from rich.console import Console as _Console
from rich.markdown import Markdown
from rich.table import Column, Table
from rich.theme import Theme

BASE_STYLE = {
    "help": "cyan",
    "bright": "white",
    "repr.str": "dim",
    "repr.brace": "dim",
    "repr.url": "blue",
    "table.header": "white",
    "toolbar.fg": "#888888",
    "toolbar.bg": "#111111",
    "toolbar.bold": "#FFFFFF",
    "error": "red",
}

def console_theme(theme_name: Union[str, None] = None) -> dict:
    """
    Return a console theme as a dictionary.

    Args:
        theme_name (str):
    """
    cfg = ConfigParser()
    cfg.read_dict({"styles": BASE_STYLE})

    if theme_name:
        theme_path = theme_name if theme_name else os.environ.get("DEFAULT_THEME", "blue_train")
        cfg.read(Theme(Path(theme_path) / Path("console.cfg")))
    return cfg["styles"]

@rich.repr.auto
class Console(_Console):
    """
    SYNOPSIS

        Subclasses a rich.console.Console to provide an instance with a
        reconfigured themes, and convenience methods and attributes.

    USAGE

        Console([ARGS])

    ARGS

        theme       The name of a theme to load. Defaults to DEFAULT_THEME.

    EXAMPLES

        Console().print("Can I kick it?")
        >>> Can I kick it?

    INSTANCE ATTRIBUTES

        theme       The current theme

    """

    def __init__(self, *args, **kwargs):
        self._console_theme = console_theme(kwargs.get("theme", None))
        self._overflow = "ellipsis"
        kwargs["theme"] = Theme(self._console_theme, inherit=False)
        super().__init__(*args, **kwargs)

        self._session = PromptSession()
    @property
    def theme(self) -> Theme:
        return self._console_theme
    def prompt(self, lines: List, **kwargs) -> str:
        """
        Print a list of lines, using the final line as a prompt.

        Example:

            Console().prompt(["Can I kick it?", "[Y/n] ")
            >>> Can I kick it?
            [Y/n]>

        """

        prompt_style = Style.from_dict(
            {
                # 'bottom-toolbar': f"{self.theme['toolbar.fg']} bg:{self.theme['toolbar.bg']}",
                # 'toolbar-bold': f"{self.theme['toolbar.bold']}"
            }
        )

        for line in lines[:-1]:
            super().print(line)
        with self.capture() as capture:
            super().print(f"[prompt bold]{lines[-1]}>[/] ", end="")
        text = ANSI(capture.get())

        # This is required to intercept key bindings and not mess up the
        # prompt. Both the prompt and bottom_toolbar params must be functions
        # for this to correctly regenerate the prompt after the interrupt.
        with patch_stdout(raw=True):
            return self._session.prompt(lambda: text, style=prompt_style, color_depth=ColorDepth.TRUE_COLOR, **kwargs)
    def mdprint(self, txt: str, **kwargs) -> None:
        """
        Like print(), but support markdown. Text will be dedented.
        """
        self.print(Markdown(dedent(txt), justify="left"), **kwargs)
    def print(self, txt: str, **kwargs) -> None:
        """
        Print text to the console, possibly truncated with an ellipsis.
        """
        super().print(txt, overflow=self._overflow, **kwargs)
    def debug(self, txt: str, **kwargs) -> None:
        """
        Print text to the console with the current theme's debug style applied, if debugging is enabled.
        """
        if os.environ.get("DEBUG", None):
            self.print(dedent(txt), style="debug")
    def error(self, txt: str, **kwargs) -> None:
        """
        Print text to the console with the current theme's error style applied.
        """
        self.print(dedent(txt), style="error")
    def table(self, *cols: List[Column], **params) -> None:
        """
        Print a rich table to the console with theme elements and styles applied.
        parameters and keyword arguments are passed to rich.table.Table.
        """
        background_style = f"on {self.theme['background']}"
        params.update(
            header_style=background_style,
            title_style=background_style,
            border_style=background_style,
            row_styles=[background_style],
            caption_style=background_style,
            style=background_style,
        )
        params["min_width"] = 80
        width = os.environ.get("CONSOLE_WIDTH", "auto")
        if width == "expand":
            params["expand"] = True
        elif width != "auto":
            params["width"] = int(width)
        return Table(*cols, **params)
