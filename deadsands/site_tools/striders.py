import random
import textwrap

from functools import cached_property

import npc

from language import types
from language.languages import lizardfolk


subspecies = [
    ('black', 'acid'),
    ('red', 'fire'),
    ('blue', 'lightning'),
    ('green', 'poison'),
    ('white', 'frost')
]

ages = types.WeightedSet(
    ('wyrmling', 0.2),
    ('young', 1.0),
    ('adult', 1.0),
    ('ancient', 0.5)
)


class SandStriderNameGenerator(types.NameGenerator):
    def __init__(self):
        super().__init__(
            language=lizardfolk.Language,
            templates=types.NameSet(
                (types.NameTemplate("name,name"), 1.0),
            ),
        )


class NPC(npc.types.NPC):

    language = lizardfolk

    has_tail = True
    has_horns = True

    def __init__(self):
        super().__init__(self)
        self._personality = ''
        self._flaw = ''
        self._goal = ''

    @cached_property
    def name(self) -> str:
        return str(SandStriderNameGenerator())

    @cached_property
    def fullname(self) -> str:
        return self.name

    @cached_property
    def age(self) -> str:
        return ages.random()

    @cached_property
    def subspecies(self) -> tuple:
        return random.choice(subspecies)

    @cached_property
    def color(self) -> str:
        return self.subspecies[0]

    @cached_property
    def spit(self) -> str:
        return self.subspecies[1]

    @property
    def description(self) -> str:
        return (
            f"{self.name} is {npc.types.a_or_an(self.age)} {self.age} {self.color} sand strider "
            f"with {self.horns} horns, {npc.types.a_or_an(self.nose)} {self.nose} snout, "
            f"{self.body} body, and {self.tail} tail. {self.name} spits {self.spit}."
        )

    @property
    def character_sheet(self) -> str:
        return '\n'.join(textwrap.wrap(self.description, width=120))
