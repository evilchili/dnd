import npc

from language import defaults, types
from language.languages import common
from random_sets.sets import equal_weights


# some old-west sounding names. The majority of NPC names will use one of these
# as a given name, but will mix in the occasional fully random name from the
# Common language base class to keep it consistent with Telisar as a whole.
given_names = equal_weights([
    'Alonzo', 'Amos', 'Arthur', 'Art', 'Austin', 'Bart', 'William', 'Bill',
    'Will', 'Boone', 'Buck', 'Butch', 'Calvin', 'Carson', 'Cassidy', 'Charlie',
    'Chester', 'Clay', 'Clayton', 'Cole', 'Coleman', 'Colt', 'Cooper', 'Coop',
    'Earle', 'Edgar', 'Ed', 'Elijah', 'Eli', 'Ernest', 'Eugene', 'Gene',
    'Flynn', 'Frank', 'Gary', 'George', 'Harry', 'Henry', 'Holt', 'Homer',
    'Howard', 'Ike', 'James', 'Jasper', 'Jesse', 'John', 'Julian', 'Kit',
    'Lawrence', 'Levi', 'Logan', 'Louis', 'Morgan', 'Porter', 'Reid', 'Reuben',
    'Rufus', 'Samuel', 'Sam', 'Thomas', 'Tom', 'Tommy', 'Virgil', 'Walter',
    'Walt', 'Wayne', 'Wesley', 'Wyatt', 'Zane', 'Zeke', 'Adelaide', 'Alice',
    'Anna', 'Annie', 'Beatrice', 'Catherine', 'Cecily', 'Clara', 'Cora',
    'Dorothea', 'Dorothy', 'Edith', 'Eleanor', 'Eliza', 'Elizabeth', 'Beth',
    'Lizzie', 'Ella', 'Emma', 'Florence', 'Gertrude', 'Gertie', 'Harriet',
    'Hazel', 'Ida', 'Josephine', 'Letitia', 'Louise', 'Lucinda', 'Lydia',
    'Mary', 'Matilda', 'Tilly', 'Maude', 'Mercy', 'Minnie', 'Olivia',
    'Rosemary', 'Sarah', 'Sophia', 'Temperance', 'Teresa', 'Tess', 'Theodora',
    'Teddy', 'Virginia', 'Ginny', 'Winifred', 'Winnie',
], blank=False)

initials = defaults.vowels + defaults.consonants


class HopperName(types.NameGenerator):
    """
    A variant on the Common name generator. In the Dewa Q'Asos region,
    nicknames are much more common, and while folks may still have multiple
    given names, they tend to use initials, or omit their middle names
    entirely.
    """
    def __init__(self):
        super().__init__(
            language=common.Language,
            templates=types.NameSet(

                # names without nicknames
                (types.NameTemplate("given,surname"), 0.5),
                (types.NameTemplate("given,initial,surname"), 0.75),
                (types.NameTemplate("given,initial,initial,surname"), 0.5),
                (types.NameTemplate("initial,given,surname"), 0.5),
                (types.NameTemplate("initial,initial,surname"), 0.5),

                # names with nickknames
                (types.NameTemplate("nickname,given,surname"), 0.75),
                (types.NameTemplate("nickname,given,initial,surname"), 0.5),
                (types.NameTemplate("nickname,given,initial,initial,surname"), 0.25),
                (types.NameTemplate("nickname,name,surname"), 0.5),
                (types.NameTemplate("nickname,name,initial,surname"), 0.25),
            ),

            # these match the default Common language name generator
            syllables=types.SyllableSet(
                (types.Syllable(template="vowel|consonant"), 1.0),
                (types.Syllable(template="consonant,vowel"), 1.0),
            ),
            suffixes=common.names.suffixes,

            # add the nicknames, for which we use the list of NPC personality traits.
            nicknames=defaults.personality + defaults.adjectives,
        )

    def get_initial(self):
        initial = ''
        while not initial:
            initial = initials.random()
        return initial.capitalize() + '.'

    def get_given(self):
        return given_names.random().capitalize()


Name = HopperName()
NobleName = Name


class Human(npc.types.NPC):
    """
    A varianat human NPC type that generates names suitable for the dead sands.
    """
    language = common

    @property
    def name(self):
        if not self._name:
            self._name = Name.name()[0]
        return self._name['fullname']


# entrypoint for class discovery
NPC = Human
