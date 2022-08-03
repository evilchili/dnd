import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from pelican.writers import Writer
from pelican.utils import slugify, sanitised_join
from site_tools import SETTINGS


def create(content_type: str, title: str, template_dir: str,
           category: str = None, template: str = None) -> str:
    """
    Return the path to a new source file.
    """
    base_path = Path(__file__).parent.absolute()

    def _slugify(s):
        return slugify(s, regex_subs=SETTINGS['SLUG_REGEX_SUBSTITUTIONS'])

    template_path = Path(template_dir)
    template_name = template + ".md"
    if not (template_path / template_name).exists():
        template_name = 'default.md'
        print("Not found. Using default markdown template.")
    template_source = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
    ).get_template(template_name)

    target_filename = _slugify(title) + '.md'

    relpath = Path(slugify(category)) if category else ''

    target_path = base_path / SETTINGS['PATH'] / relpath
    dest = sanitised_join(str(target_path / target_filename))

    SETTINGS['WRITE_SELECTED'].append(dest)
    writer = Writer(target_path, settings=SETTINGS)
    writer.write_file(name=target_filename, template=template_source, context={
        'title': title,
        'tags': content_type,
        'date': datetime.datetime.now(),
        'filename': str(relpath / target_filename)
    })
    return dest
