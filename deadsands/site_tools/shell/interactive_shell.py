from pathlib import Path

from prompt_toolkit.application import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from rich.table import Table
from rolltable.tables import RollTable

from site_tools.shell.base import BasePrompt, command

BINDINGS = KeyBindings()

class DMShell(BasePrompt):
    def __init__(self, cache={}):
        super().__init__(cache)
        self._name = "DM Shell"
        self._prompt = ["dm"]
        self._toolbar = [("class:bold", " DMSH ")]
        self._key_bindings = BINDINGS
        self._register_subshells()
        self._register_keybindings()

    def _register_keybindings(self):
        self._toolbar.extend(
            [
                ("", " [?] Help "),
                ("", " [F2] Wild Magic Table "),
                ("", " [^Q] Quit "),
            ]
        )

        @self.key_bindings.add("c-q")
        @self.key_bindings.add("c-d")
        @self.key_bindings.add("<sigint>")
        def quit(event):
            self.quit()

        @self.key_bindings.add("?")
        def help(event):
            self.help()

        @self.key_bindings.add("f2")
        def wmt(event):
            self.wmt()

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
        try:
            get_app().exit()
        finally:
            raise SystemExit("")
    @command(usage="""
    [title]HELP FOR THE HELP LORD[/title]

    The [b]help[/b] command will print usage information for whatever you're currently
    doing. You can also ask for help on any command currently available.

    [title]USAGE[/title]

        [link]> help [COMMAND][/link]
    """)
    def help(self, parts=[]):
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
    def id(self, parts=[]):
        """
        Increment the date by one day.
        """
        raise NotImplementedError()
    @command(
        usage="""
    [title]LOCATION[/title]

    [b]loc[/b] sets the party's location to the specified region of the Sahwat Desert.

    [title]USAGE[/title]

        [link]loc LOCATION[/link]
    """,
        completer=WordCompleter(["The Blooming Wastes", "Dust River Canyon", "Gopher Gulch", "Calamity Ridge"]),
    )
    def loc(self, parts=[]):
        """
        Move the party to a new region of the Sahwat Desert.
        """
        if parts:
            self.cache["location"] = " ".join(parts)
        self.console.print(f"The party is in {self.cache['location']}.")
    @command(usage="""
    [title]OVERLAND TRAVEL[/title]

    [b]ot[/b]

    [title]USAGE[/title]

        [link]ot in[/link]
    """)
    def ot(self, parts=[]):
        """
        Increment the date by one day and record
        """
        raise NotImplementedError()
    @command(usage="""
    [title]WILD MAGIC TABLE[/title]

    [b]wmt[/b] Generates a d20 wild magic surge roll table. The table will be cached for the cache.

    [title]USAGE[/title]

        [link]> wmt[/link]

    [title]CLI[/title]

        [link]roll-table \\
                sources/sahwat_magic_table.yaml \\
                --frequency default --die 20[/link]
    """)
    def wmt(self, *parts, source="sahwat_magic_table.yaml"):
        """
        Generate a Wild Magic Table for resolving spell effects.
        """
        if "wmt" not in self.cache:
            rt = RollTable(
                [Path(f"{self.cache['table_sources_path']}/{source}").read_text()],
                frequency="default",
                die=20,
            )
            table = Table(*rt.expanded_rows[0])
            for row in rt.expanded_rows[1:]:
                table.add_row(*row)
            self.cache["wmt"] = table
        self.console.print(self.cache["wmt"])
