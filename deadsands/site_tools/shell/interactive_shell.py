from pathlib import Path

from prompt_toolkit.application import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from rich.table import Table
from rolltable.tables import RollTable

from site_tools.shell.base import BasePrompt, command
from site_tools import campaign
from site_tools import jobs

from npc.generator.base import generate_npc
from reckoning.calendar import TelisaranCalendar
from reckoning.telisaran import Day
from reckoning.telisaran import ReckoningError

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

        self.cache['campaign'] = campaign.load(
            path=self.cache['campaign_save_path'],
            name=self.cache['campaign_name'],
            start_date=self.cache['campaign_start_date'],
            console=self.console
        )
        self._campaign = self.cache['campaign']

    def _register_keybindings(self):
        self._toolbar.extend(
            [
                ("", " [?] Help "),
                ("", " [F2] Wild Magic Table "),
                ("", " [F3] Trinkets"),
                ("", " [F4] NPC"),
                ("", " [F5] Date"),
                ("", " [F6] Job"),
                ("", " [F8] Save"),
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

        @self.key_bindings.add("f3")
        def trinkets(event):
            self.trinkets()

        @self.key_bindings.add("f4")
        def npc(event):
            self.npc()

        @self.key_bindings.add("f5")
        def date(event):
            self.date()

        @self.key_bindings.add("f6")
        def job(event):
            self.job()

        @self.key_bindings.add("f8")
        def save(event):
            self.save()

    def _handler_date_season(self, *args):
        self.console.print(self.cache['calendar'].season)

    def _handler_date_year(self, *args):
        self.console.print(self.cache['calendar'].calendar)

    def _handler_date_inc(self, days):
        offset = int(days or 1) * Day.length_in_seconds
        self._campaign['date'] = self._campaign['date'] + offset
        return self.date()

    def _handler_date_dec(self, days):
        offset = int(days or 1) * Day.length_in_seconds
        self._campaign['date'] = self._campaign['date'] - offset
        return self.date()

    def _handler_date_set(self, new_date):
        try:
            self._campaign['date'] = campaign.string_to_date(new_date)
        except ReckoningError as e:
            self.console.error(str(e))
            self.console.error("Invalid date. Use numeric formats; see 'help date' for more.")
        self.cache['calendar'] = TelisaranCalendar(today=self._campaign['date'])
        return self.date()

    def _rolltable(self, source, frequency='default', die=20):
        rt = RollTable(
            [Path(f"{self.cache['table_sources_path']}/{source}").read_text()],
            frequency=frequency,
            die=die
        )
        table = Table(*rt.rows[0])
        for row in rt.rows[1:]:
            table.add_row(*row)
        return table

    @command(usage="""
    [title]DATE[/title]

    Work with the Telisaran calendar, including the current campaign date.

    [title]USAGE[/title]

        [link]> date [COMMAND[, ARGS]][/link]

        COMMAND     Description

        season      Print the spans of the current season, highlighting today
        year        Print the full year's calendar, highlighting today.
        inc N       Increment the current date by N days; defaults to 1.
        dec N       Decrement the current date by N days; defaults to 1.
        set DATE    Set the current date to DATE, in numeric format, such as
                    [link]2.1125.1.45[/link].
    """, completer=WordCompleter(
        [
            'season',
            'year',
            'inc',
            'dec',
            'set',
        ]
    ))
    def date(self, parts=[]):

        if not self.cache['calendar']:
            self.cache['calendar'] = TelisaranCalendar(today=self._campaign['date'])

        if not parts:
            self.console.print(f"Today is {self._campaign['date'].short} ({self._campaign['date'].numeric})")
            return

        cmd = parts[0]
        try:
            val = parts[1]
        except IndexError:
            val = None

        handler = getattr(self, f"_handler_date_{cmd}", None)
        if not handler:
            self.console.error(f"Unsupported command: {cmd}. Try 'help date'.")
            return

        return handler(val)

    @command(usage="""
    [title]Save[/title]

    Save the campaign state.

    [title]USAGE[/title]

        [link]> save[/link]
    """)
    def save(self, parts=[]):
        """
        Save the campaign state.
        """
        path, count = campaign.save(
            self.cache['campaign'],
            path=self.cache['campaign_save_path'],
            name=self.cache['campaign_name']
        )
        self.console.print(f"Saved {path}; {count} backups exist.")

    @command(usage="""
    [title]NPC[/title]

    Generate a randomized NPC commoner.

    [title]USAGE[/title]

        [link]> npc \\[ANCESTRY\\][/link]

    [title]CLI[/title]

        [link]npc --ancestry ANCESTRY[/link]
    """, completer=WordCompleter(
        [
            'human',
            'dragon',
            'drow',
            'dwarf',
            'elf',
            'highelf',
            'halfling',
            'halforc',
            'tiefling',
            'hightiefling',
        ]
    ))
    def npc(self, parts=[]):
        """
        Generate an NPC commoner
        """
        c = generate_npc(ancestry=parts[0] if parts else None)
        self.console.print("\n".join([
            "",
            f"{c.description}",
            f"Personality: {c.personality}",
            f"Flaw:        {c.flaw}",
            f"Goal:        {c.goal}",
            "",
        ]))

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
        self.save()
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

    @command(
        usage="""
    [title]LOCATION[/title]

    [b]loc[/b] sets the party's location to the specified region of the Sahwat Desert.

    [title]USAGE[/title]

        [link]loc LOCATION[/link]
    """,
        completer=WordCompleter(
            [
                "The Blooming Wastes",
                "Dust River Canyon",
                "Gopher Gulch",
                "Calamity Ridge"
            ]
        ),
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
    def wmt(self, parts=[], source="sahwat_magic_table.yaml"):
        """
        Generate a Wild Magic Table for resolving spell effects.
        """
        if "wmt" not in self.cache:
            self.cache['wmt'] = self._rolltable(source)
        self.console.print(self.cache['wmt'])

    @command(usage="""
    [title]TRINKET TABLE[/title]

    [b]trinkets[/b] Generates a d20 random trinket table.

    [title]USAGE[/title]

        [link]> trinkets[/link]

    [title]CLI[/title]

        [link]roll-table \\
                sources/trinkets.yaml \\
                --frequency default --die 20[/link]
    """)
    def trinkets(self, parts=[], source="trinkets.yaml"):
        self.console.print(self._rolltable(source))

    @command(usage="""
    [title]LEVEL[/title]

    Get or set the current campaign's level. Used for generating loot tables.

    [title]USAGE[/title]

        [link]> level [LEVEL][/link]

    """)
    def level(self, parts=[]):
        if parts:
            newlevel = int(parts[0])
            if newlevel > 20 or newlevel < 1:
                self.console.error(f"Invalid level: {newlevel}. Levels must be between 1 and 20.")
            self._campaign['level'] = newlevel
        self.console.print(f"Party is currently at level {self._campaign['level']}.")

    @command(usage="""
    [title]JOB[/title]

    Generate a random job.

    [title]USAGE[/title]

        [link]> job[/link]

    """)
    def job(self, parts=[]):
        self.console.print(jobs.generate_job())

