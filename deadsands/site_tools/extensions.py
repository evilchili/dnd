import textwrap
from rolltable.tables import RollTable as _RT
from jinja2_simple_tags import StandaloneTag
from pathlib import Path


class RollTable(StandaloneTag):
    tags = {"rolltable"}

    def render(self, sources, frequency='default', die=8, indent=0, **kwargs):
        rt = _RT([Path(f'sources/{s}.yaml').read_text() for s in sources],
                 frequency=frequency, die=die)
        return textwrap.indent(rt.as_yaml(), ' ' * indent)
