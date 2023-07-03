import functools
from collections import namedtuple, defaultdict

from prompt_toolkit.completion import NestedCompleter


from site_tools.console import Console
from textwrap import dedent

COMMANDS = defaultdict(dict)

Command = namedtuple('Commmand', 'prompt,handler,usage,completer')


def register_command(handler, usage, completer=None):
    prompt = handler.__qualname__.split('.', -1)[0]
    cmd = handler.__name__
    if cmd not in COMMANDS[prompt]:
        COMMANDS[prompt][cmd] = Command(
            prompt=prompt,
            handler=handler,
            usage=usage,
            completer=completer,
        )


def command(usage, completer=None, binding=None):
    def decorator(func):
        register_command(func, usage, completer)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


class BasePrompt(NestedCompleter):

    def __init__(self, console=None):
        super(BasePrompt, self).__init__(self._nested_completer_map())

        self._prompt = ''
        self._autocomplete_values = []
        self._console = None
        self._theme = None

    def _nested_completer_map(self):
        return dict(
            (cmd_name, cmd.completer) for (cmd_name, cmd) in COMMANDS[self.__class__.__name__].items()
        )

    def _get_help(self, cmd=None):
        try:
            return dedent(COMMANDS[self.__class__.__name__][cmd].usage)
        except KeyError:
            return self.usage

    def default_completer(self, document, complete_event):
        raise NotImplementedError(f"Implement the 'default_completer' method of {self.__class__.__name__}")

    @property
    def usage(self):
        text = dedent("""
        [title]dmsh[/title]

        Available commands are listed below. Try 'help COMMAND' for detailed help.

        [title]COMMANDS[/title]

        """)
        for (name, cmd) in sorted(self.commands.items()):
            text += f"    [b]{name:10s}[/b]    {cmd.handler.__doc__.strip()}\n"
        return text

    @property
    def commands(self):
        return COMMANDS[self.__class__.__name__]

    @property
    def console(self):
        if not self._console:
            self._console = Console(color_system='truecolor')
        return self._console

    @property
    def prompt(self):
        return self._prompt

    @property
    def autocomplete_values(self):
        return self._autocomplete_values

    @property
    def toolbar(self):
        return None

    @property
    def key_bindings(self):
        return None

    def help(self, parts):
        attr = None
        if parts:
            attr = parts[0]
        self.console.print(self._get_help(attr))
        return True

    def process(self, cmd, *parts):
        if cmd in self.commands:
            return self.commands[cmd].handler(self, parts)
        self.console.error(f"Command {cmd} not understood.")

    def start(self, cmd=None):
        while True:
            if not cmd:
                cmd = self.console.prompt(
                    self.prompt,
                    completer=self,
                    bottom_toolbar=self.toolbar,
                    key_bindings=self.key_bindings)
            if cmd:
                cmd, *parts = cmd.split()
                self.process(cmd, *parts)
            cmd = None
