import click
import os
import shutil
import subprocess
import sys
import typer
import webbrowser

from enum import Enum
from livereload import Server
from pelican import main as pelican_main
from site_tools import SETTINGS, DEV_SETTINGS_FILE_BASE, PUB_SETTINGS_FILE_BASE
from site_tools.content_manager import create

CONFIG = {
    'settings_base': DEV_SETTINGS_FILE_BASE,
    'settings_publish': PUB_SETTINGS_FILE_BASE,
    # Output path. Can be absolute or relative to tasks.py. Default: 'output'
    'deploy_path': SETTINGS['OUTPUT_PATH'],
    # Remote server configuration
    'ssh_user': 'greg',
    'ssh_host': 'froghat.club',
    'ssh_port': '22',
    'ssh_path': '/usr/local/deploy/deadsands/',
    # Host and port for `serve`
    'host': 'localhost',
    'port': 8000,
    # content manager config
    'templates_path': 'markdown-templates',
}

app = typer.Typer()


class ContentType(str, Enum):
    post = 'post'
    lore = 'lore'
    monster = 'monster'
    region = 'region'
    page = 'page'


def pelican_run(cmd: list = [], publish=False) -> None:
    settings = CONFIG['settings_publish' if publish else 'settings_base']
    pelican_main(['-s', settings] + cmd)


@app.command()
def clean() -> None:
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])


@app.command()
def build() -> None:
    pelican_run()


@app.command()
def serve() -> None:

    url = 'http://{host}:{port}/'.format(**CONFIG)

    def cached_build():
        pelican_run(['-e', 'CACHE_CONTENT=true', 'LOAD_CONTENT_CACHE=true',
                     'SHOW_DRAFTS=true', f'SITEURL="{url}"'])

    clean()
    cached_build()
    server = Server()
    theme_path = SETTINGS['THEME']
    watched_globs = [
        CONFIG['settings_base'],
        '{}/templates/**/*.html'.format(theme_path),
    ]

    content_file_extensions = ['.md', '.rst']
    for extension in content_file_extensions:
        content_glob = '{0}/**/*{1}'.format(SETTINGS['PATH'], extension)
        watched_globs.append(content_glob)

    static_file_extensions = ['.css', '.js']
    for extension in static_file_extensions:
        static_file_glob = '{0}/static/**/*{1}'.format(theme_path, extension)
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if OPEN_BROWSER_ON_SERVE:
        webbrowser.open(url)

    server.serve(host=CONFIG['host'], port=CONFIG['port'],
                 root=CONFIG['deploy_path'])


@app.command()
def publish() -> None:
    clean()
    pelican_run(publish=True)
    subprocess.call(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        '{} {ssh_user}@{ssh_host}:{ssh_path}'.format(
            CONFIG['deploy_path'].rstrip('/') + '/',
            **CONFIG
        )
    )


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
