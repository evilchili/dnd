import asyncio
import sys
import termios
from enum import Enum
from pathlib import Path

import click
import typer
from rolltable.tables import RollTable
from typing_extensions import Annotated

from site_tools.content_manager import create
from site_tools.shell.interactive_shell import DMShell
from site_tools import build_system


class ContentType(str, Enum):
    post = "post"
    lore = "lore"
    monster = "monster"
    region = "region"
    location = "location"
    page = "page"


class Die(str, Enum):
    d100 = "100"
    d20 = "20"
    d12 = "12"
    d10 = "10"
    d6 = "6"
    d4 = "4"


# 'site' ENTRY POINT
site_app = typer.Typer()


# BUILD SYSTEM SUBCOMMANDS

@site_app.command()
def clean() -> None:
    build_system.clean()


@site_app.command()
def build() -> None:
    build_system.build()


@site_app.command()
def watch() -> None:
    build_system.watch()


@site_app.command()
def serve() -> None:
    build_system.serve()


@site_app.command()
def publish() -> None:
    build_system.publish()


# CONTENT MANAGEMENT COMMANDS

@site_app.command()
def restock(
    source: str = typer.Argument(..., help="The source file for the store."),
    frequency: str = Annotated[str, typer.Option("default", help="use the specified frequency from the source file")],
    die: Die = typer.Option(20, help="The size of the die for which to create a table"),
    template_dir: str = Annotated[
        str,
        typer.Argument(
            build_system.CONFIG["templates_path"],
            help="Override the default location for markdown templates.",
        ),
    ],
) -> None:
    rt = RollTable([Path(source).read_text()], frequency=frequency, die=die, hide_rolls=True)
    store = rt.datasources[0].metadata["store"]

    click.edit(
        filename=create(
            content_type="post",
            title=store["title"],
            template_dir=template_dir,
            category="stores",
            template="store",
            extra_context=dict(inventory=rt.as_markdown, **store),
        )
    )


@site_app.command()
def new(
    content_type: ContentType = typer.Argument(
        ...,
        help="The type of content to create.",
    ),
    title: str = typer.Argument(
        ...,
        help="The title of the content.",
    ),
    category: str = typer.Argument(
        None,
        help='Override the default category; required for "post" content.',
    ),
    template: str = typer.Argument(
        None,
        help="Override the default template for the content_type.",
    ),
    template_dir: str = typer.Argument(
        build_system.CONFIG["templates_path"],
        help="Override the default location for markdown templates.",
    ),
) -> None:
    if not category:
        match content_type:
            case "post":
                print("You must specify a category for 'post' content.")
                sys.exit()
            case "monster":
                category = "bestiary"
            case "region":
                category = "locations"
            case "location":
                category = "locations"
            case "page":
                category = "pages"
            case _:
                category = content_type.value
    click.edit(filename=create(content_type.value, title, template_dir, category, template or content_type.value))


# STANDALONE ENTRY POINTS

def dmsh():
    old_attrs = termios.tcgetattr(sys.stdin)
    try:
        asyncio.run(DMShell(build_system.CONFIG).start())
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSANOW, old_attrs)


if __name__ == "__main__":
    site_app()
