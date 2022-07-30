import yaml
import random
from collections.abc import Generator
from typing import Optional, Mapping, List


class RollTable:
    """
    Generate a roll table using weighted distributions of random options.

    Usage:

    Given source.yaml containing options such as:

        option1:
            - key1: description
            - key2: description
            ...
        ...

    Generate a random table:

        >>> print(RollTable(path='source.yaml'))
        d1    option6    key3   description
        d2    option2    key2   description
        d3    option3    key4   description
        ...

    You can customize the frequency distribution, headers, and table size by
    defining metadata in your source file.

    Using Metadata:

    By default options are given uniform distribution and random keys will be
    selected from each option with equal probability. This behaviour can be
    changed by adding an optional metadata section to the source file:

        metadata:
          frequenceis:
            default:
              option1: 0.5
              option2: 0.1
              option3: 0.3
              option4: 0.1

    This will guarantee that random keys from option1 are selected 50% of the
    time, from option 2 10% of the time, and so forth. Frequencies should add
    up to 1.0.

    If the metadata section includes 'frequencies', The 'default' distribution
    must be defined. Additional optional distributions may also be defined, if
    you want to provide alternatives for specific use cases.

        metadata:
          frequenceis:
            default:
              option1: 0.5
              option2: 0.1
              option3: 0.3
              option4: 0.1
            inverted:
              option1: 0.1
              option2: 0.3
              option3: 0.1
              option4: 0.5

    A specific frequency distribution can be specifed by passing the 'frequency'
    parameter at instantiation:

        >>> t = RollTable('source.yaml', frequency='inverted')

    The metadata section can also override the default size of die to use for
    the table (a d20). For example, this creates a 100-row table:

        metadata:
          die: 100

    This too can be overridden at instantiation:

        >>> t = RollTable('source.yaml', die=64)

    Finally, headers for your table columns can also be defined in metadata:

        metadata:
          headers:
              - Roll
              - Category
              - Description
              - Effect

     This will yield output similar to:

        >>> print(RollTable(path='source.yaml'))
        Roll  Category   Name   Effect
        d1    option6    key3   description
        d2    option2    key2   description
        d3    option3    key4   description
        ...
    """

    def __init__(self, path: str, frequency: str = 'default',
                 die: Optional[int] = None, collapsed: bool = True):
        """
        Initialize a RollTable instance.

        Args:
            path        - the path to the source file
            frequency   - the name of the frequency distribution to use; must
                          be defined in the source file's metadata.
            die         - specify a die size
            collapsed   - If True, collapse multiple die values with the same
                          options into a single line.
        """
        self._path = path
        self._frequency = frequency
        self._die = die
        self._collapsed = collapsed
        self._metadata = None
        self._source = None
        self._values = None

    def _load_source(self) -> None:
        """
        Cache the yaml source and parsed or generated the metadata.
        """
        if self._source:
            return
        with open(self._path, 'r') as source:
            self._source = yaml.safe_load(source)

        def _defaults():
            num_keys = len(self._source.keys())
            default_freq = num_keys/100
            return {
                'headers': [''] * num_keys,
                'die': self._die,
                'frequencies': {
                    'default': [(k, default_freq) for k in self._source.keys()]
                }
            }
        self._metadata = self._source.pop('metadata', _defaults())

    def _collapsed_lines(self) -> Generator[list]:
        """
        Generate an array of column values for each row of the table but
        sort the values and squash multiple rows with the same values into one,
        with a range for the die roll instead of a single die. That is,

            d1 foo bar baz
            d2 foo bar baz

        becomes

            d1-d2 foo bar baz
        """
        def collapsed(last_val, offset, val, i):
            (cat, option) = last_val
            (k, v) = list(*option.items())
            if offset + 1 == i:
                return [f'd{i}', cat, k, v]
            else:
                return [f'd{offset+1}-d{i}', cat, k, v]

        last_val = None
        offset = 0
        for (i, val) in enumerate(self.values):
            if not last_val:
                last_val = val
                offset = i
                continue
            if val != last_val:
                yield collapsed(last_val, offset, val, i)
                last_val = val
                offset = i
        yield collapsed(last_val, offset, val, i+1)

    @property
    def freqtable(self):
        return self.metadata['frequencies'][self._frequency]

    @property
    def source(self) -> Mapping:
        """
        The parsed source data
        """
        if not self._source:
            self._load_source()
        return self._source

    @property
    def metadata(self) -> Mapping:
        """
        The parsed or generated metadata
        """
        if not self._metadata:
            self._load_source()
        return self._metadata

    @property
    def values(self) -> List:
        """
        Randomly pick values from the source data following the frequency
        distrubtion of the options.
        """
        if not self._values:
            weights = []
            options = []
            for (option, weight) in self.freqtable.items():
                weights.append(weight)
                options.append(option)
            freqs = random.choices(options, weights=weights,
                                   k=self._die or self.metadata['die'])
            self._values = []
            for option in freqs:
                self._values += [(option, random.choice(self.source[option]))]
            return sorted(self._values, key=lambda val: list(val[1].values())[0])

    @property
    def lines(self) -> Generator[List]:
        """
        Yield a list of table rows suitable for formatting as output.
        """
        yield self.metadata['headers']

        if self._collapsed:
            for line in self._collapsed_lines():
                yield line
        else:
            for (i, item) in enumerate(self.values):
                (cat, option) = item
                (k, v) = list(option.items())[0]
                yield [f'd{i+1}', cat, k, v]

    def __str__(self) -> str:
        """
        Return the lines as a single string.
        """
        return "\n".join([
            '{:10s}\t{:8s}\t{:20s}\t{:s}'.format(*line) for line in self.lines
        ])


if __name__ == '__main__':
    import sys
    print(RollTable(path=sys.argv[1], die=int(sys.argv[2])))
