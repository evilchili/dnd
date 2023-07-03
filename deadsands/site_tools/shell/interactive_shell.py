from site_tools.shell.base import BasePrompt, command
from rolltable.tables import RollTable
from rich.table import Table
from pathlib import Path
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app


bindings = KeyBindings()


class InteractiveShell(BasePrompt):

    def __init__(self, prompt=[], config={}, session={}):
        super().__init__()
        self._prompt = prompt
        self._config = config
        self._wmt = ""
        self._subshells = {}
        self._register_subshells()
        self._register_keybindings()
        self._session = session

    def _register_keybindings(self):

        @bindings.add('c-q')
        @bindings.add('c-d')
        def quit(event):
            self.quit()

        @bindings.add('c-h')
        def help(event):
            self.help()

        @bindings.add('c-w')
        def wmt(event):
            self.wmt()

    def _register_subshells(self):
        for subclass in BasePrompt.__subclasses__():
            if subclass.__name__ == self.__class__.__name__:
                continue
            self._subshells[subclass.__name__] = subclass(parent=self)

    @property
    def key_bindings(self):
        return bindings

    @property
    def toolbar(self):
        return [
            ('class:bold', ' DMSH '),
            ('', " [H]elp "),
            ('', " [W]mt "),
            ('', " [Q]uit "),
        ]

    @property
    def session(self):
        return self._session

    @property
    def autocomplete_values(self):
        return list(self.commands.keys())

    def default_completer(self, document, complete_event):  # pragma: no cover
        word = document.current_line_before_cursor
        raise Exception(word)

    def process(self, cmd, *parts):
        if cmd in self.commands:
            return self.commands[cmd].handler(self, parts)
        return "Unknown Command; try help."

    @command(usage="""
    [title]QUIT[/title]

    The [b]quit[/b] command exits dmsh.

    [title]USAGE[/title]

        [link]> quit|^D|<ENTER>[/link]
    """)
    def quit(self, *parts):
        """
        Quit dmsh.
        """
        get_app().exit()
        raise SystemExit("Okay BYEEEE")

    @command(usage="""
    [title]HELP FOR THE HELP LORD[/title]

    The [b]help[/b] command will print usage information for whatever you're currently
    doing. You can also ask for help on any command currently available.

    [title]USAGE[/title]

        [link]> help [COMMAND][/link]
    """)
    def help(self, *parts):
        """
        Display the help message.
        """
        super().help(parts)
        return True

    @command(usage="""
    [title]INCREMENT DATE[/title]

    [b]id[/b] Increments the calendar date by one day.

    [title]USAGE[/title]

        [link]id[/link]
    """)
    def id(self, *parts):
        """
        Increment the date by one day.
        """
        raise NotImplementedError()

    @command(usage="""
    [title]LOCATION[/title]

    [b]loc[/b] sets the party's location to the specified region of the Sahwat Desert.

    [title]USAGE[/title]

        [link]loc LOCATION[/link]
    """,
             completer=WordCompleter([
                "The Blooming Wastes",
                "Dust River Canyon",
                "Gopher Gulch",
                "Calamity Ridge"
             ]))
    def loc(self, *parts):
        """
        Move the party to a new region of the Sahwat Desert.
        """
        if parts:
            self.session['location'] = (' '.join(parts))
        self.console.print(f"The party is in {self.session['location']}.")

    @command(usage="""
    [title]OVERLAND TRAVEL[/title]

    [b]ot[/b]

    [title]USAGE[/title]

        [link]ot in[/link]
    """)
    def ot(self, *parts):
        """
        Increment the date by one day and record
        """
        raise NotImplementedError()

    @command(usage="""
    [title]WILD MAGIC TABLE[/title]

    [b]wmt[/b] Generates a d20 wild magic surge roll table. The table will be cached for the session.

    [title]USAGE[/title]

        [link]> wmt[/link]

    [title]CLI[/title]

        [link]roll-table \\
                sources/sahwat_magic_table.yaml \\
                --frequency default --die 20[/link]
    """)
    def wmt(self, *parts, source='sahwat_magic_table.yaml'):
        """
        Generate a Wild Magic Table for resolving spell effects.
        """
        if not self._wmt:
            rt = RollTable(
                [Path(f"{self._config['table_sources_path']}/{source}").read_text()],
                frequency='default',
                die=20,
            )
            table = Table(*rt.expanded_rows[0])
            for row in rt.expanded_rows[1:]:
                table.add_row(*row)
            self._wmt = table
        self.console.print(self._wmt)
