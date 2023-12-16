import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pelican.utils import sanitised_join, slugify
from pelican.writers import Writer
from pprint import pprint as print

from site_tools import SETTINGS


def create(
    content_type: str,
    title: str,
    template_dir: str,
    category: str = None,
    source: str = None,
    template: str = None,
    extra_context: dict = {},
) -> str:
    """
    Return the path to a new source file.
    """
    base_path = Path.cwd()

    def _slugify(s):
        return slugify(s, regex_subs=SETTINGS["SLUG_REGEX_SUBSTITUTIONS"])
    template_path = Path(template_dir)
    template_name = f"{template or content_type}.md"
    if not (template_path / template_name).exists():
        print(f"Expected template {template_name} not found. Using default markdown template.")
        template_name = "default.md"
    env = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
    )
    env.add_extension("site_tools.extensions.RollTable")
    template_source = env.get_template(template_name)

    target_filename = _slugify(title) + ".md"

    relpath = Path(slugify(category)) if category else ""

    target_path = base_path / SETTINGS["PATH"] / relpath
    dest = sanitised_join(str(target_path / target_filename))

    #SETTINGS["WRITE_SELECTED"].append(dest)
    writer = Writer(target_path, settings=SETTINGS)
    writer.write_file(
        name=target_filename,
        template=template_source,
        context={
            "title": title,
            "tags": content_type,
            "date": datetime.datetime.now(),
            "filename": str(relpath / target_filename),
            **extra_context,
        },
    )
    return dest
