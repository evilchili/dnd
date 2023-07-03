from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.completion import FuzzyWordCompleter
from site_tools.cli import app
from enum import EnumMeta
from inspect import signature
from rich import print


def dmsh():

    session = PromptSession()

    def cmd2dict(cmd):
        sig = signature(cmd)
        if not sig.parameters:
            return None
        cmds = {}
        for (k, v) in list(sig.parameters.items()):
            print(v, dir(v))
            if v.annotation.__class__ == EnumMeta:
                cmds[k] = FuzzyWordCompleter([e.value for e in v.annotation])
            else:
                cmds[k] = None
        return cmds

    commands = dict(
        site=dict((c.callback.__name__, cmd2dict(c.callback)) for c in app.registered_commands)
    )
    print(commands)
    completer = NestedCompleter.from_nested_dict(commands)
    text = session.prompt("DM> ", completer=completer, complete_while_typing=True, enable_history_search=False)
    words = text.split()

    print(f"You said {words}")
