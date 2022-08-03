import click
import sys
import typer

from enum import Enum
from site_tools.tasks import CONFIG
from site_tools.content_manager import create

CONFIG.update(
    templates_path='markdown-templates',
)

app = typer.Typer()


class ContentType(str, Enum):
    post = 'post'
    lore = 'lore'
    monster = 'monster'
    region = 'region'
    page = 'page'


@app.command()
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
        CONFIG['templates_path'],
        help="Override the default location for markdown templates.",
    )
) -> None:
    if not category:
        match content_type:
            case 'post':
                print("You must specify a category for 'post' content.")
                sys.exit()
            case 'monster':
                category = 'beastiary'
            case 'region':
                category = 'regions'
            case _:
                category = content_type
    click.edit(filename=create(content_type, title, template_dir, category,
                               template or content_type))


if __name__ == '__main__':
    app()
