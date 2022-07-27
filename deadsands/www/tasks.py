# -*- coding: utf-8 -*-

import os
import inspect
import shlex
import shutil
import datetime

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from invoke import task
from invoke.main import program
from pelican import main as pelican_main
from pelican.writers import Writer
from pelican.utils import slugify, sanitised_join
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

OPEN_BROWSER_ON_SERVE = True
SETTINGS_FILE_BASE = 'pelicanconf.py'
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)

CONFIG = {
    'settings_base': SETTINGS_FILE_BASE,
    'settings_publish': 'publishconf.py',
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
}


@task
def clean(c):
    """Remove generated files"""
    if os.path.isdir(CONFIG['deploy_path']):
        shutil.rmtree(CONFIG['deploy_path'])
        os.makedirs(CONFIG['deploy_path'])


@task
def build(c):
    """Build local version of site"""
    pelican_run('-s {settings_base}'.format(**CONFIG))


@task
def rebuild(c):
    """`build` with the delete switch"""
    pelican_run('-d -s {settings_base}'.format(**CONFIG))


@task
def regenerate(c):
    """Automatically regenerate site upon file modification"""
    pelican_run('-r -s {settings_base}'.format(**CONFIG))


@task
def serve(c):
    """Serve site at http://$HOST:$PORT/ (default is localhost:8000)"""
    pelican_run('-rl -b {host} -p {port} --relative-urls -D --ignore-cache '
                '-s {settings_base} -e SHOW_DRAFTS="true"'.format(**CONFIG))


@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)


@task
def preview(c):
    """Build production version of site"""
    pelican_run('-s {settings_publish}'.format(**CONFIG))


@task
def livereload(c):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    def cached_build():
        cmd = '-s {settings_base} -e CACHE_CONTENT=True LOAD_CONTENT_CACHE=True'
        pelican_run(cmd.format(**CONFIG))

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
        # Open site in default browser
        import webbrowser
        webbrowser.open("http://{host}:{port}".format(**CONFIG))

    server.serve(host=CONFIG['host'], port=CONFIG['port'], root=CONFIG['deploy_path'])


@task
def publish(c):
    """Publish to production via rsync"""
    pelican_run('-s {settings_publish}'.format(**CONFIG))
    c.run(
        'rsync --delete --exclude ".DS_Store" -pthrvz -c '
        '-e "ssh -p {ssh_port}" '
        '{} {ssh_user}@{ssh_host}:{ssh_path}'.format(
            CONFIG['deploy_path'].rstrip('/') + '/',
            **CONFIG))


@task
def monster(c, name, t='default'):
    """Create a new monster"""
    return create_new_content(c, name, template=t, category='beastiary')


@task
def lore(c, title, t='default'):
    """Create a new lore post"""
    return create_new_content(c, title, template=t, category='lore')


@task
def post(c, category, title, t=None, template_dir='markdown-templates'):
    """Create a new post in the specified category"""
    return create_new_content(c, title, template=t or category, template_dir=template_dir, category=category)


@task
def page(c, title, t='default', template_dir='markdown-templates'):
    """Create a new page"""
    return create_new_content(c, title, template=t, template_dir=template_dir, output_path='pages')


def create_new_content(c, title, template_dir='markdown-templates', category="", template=None, output_path=''):
    """Create new content of a given type and invoke the editor."""

    content_type = template or inspect.stack()[1].function
    print(f"Creating new '{content_type}' content: \"{category}/{title}\"")

    base_path = Path(__file__).parent.absolute()

    def _slugify(s):
        return slugify(s, regex_subs=DEFAULT_CONFIG['SLUG_REGEX_SUBSTITUTIONS'])

    template_path = Path(template_dir)
    template_name = _slugify(content_type) + ".md"
    if not (template_path / template_name).exists():
        template_name = 'default.md'
        print("Using default markdown template.")

    target_filename = _slugify(title) + '.md'
    target_path = base_path / SETTINGS['PATH']
    if output_path:
        target_path = target_path / output_path
    if category:
        target_path = target_path / slugify(category)

    template = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
    ).get_template(template_name)

    dest = sanitised_join(str(target_path / target_filename))
    SETTINGS['WRITE_SELECTED'].append(dest)
    writer = Writer(target_path, settings=SETTINGS)
    writer.write_file(name=target_filename, template=template, context={
        'title': title,
        'tags': content_type,
        'date': datetime.datetime.now(),
        'filename': dest
    })
    c.run(f"$EDITOR {dest}", pty=True)


def pelican_run(cmd):
    cmd += ' ' + program.core.remainder  # allows to pass-through args to pelican
    pelican_main(shlex.split(cmd))
