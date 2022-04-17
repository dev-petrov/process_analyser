import sys

from .commands import CollectCommand, DetectCommand, ImportCommand, ShellCommand
from .commands.base_command import BaseCommand


class Detector: # pragma: no cover
    available_commands = {
        "import": ImportCommand,
        "detect": DetectCommand,
        "collect": CollectCommand,
        "shell": ShellCommand,
    }

    def execute(self) -> None:
        if len(sys.argv) == 1:
            sys.stderr.write("You should define command.\n")
            sys.stderr.write(f"Available commands: {', '.join(self.available_commands)}\n")
            sys.exit(1)
        subcommand = sys.argv[1]
        self.fetch_command(subcommand).run_from_argv(sys.argv)

    def fetch_command(self, subcommand) -> BaseCommand:
        try:
            command_cls = self.available_commands[subcommand]
        except KeyError:
            sys.stderr.write("Unknown command: %r" % subcommand)
            sys.exit(1)
        return command_cls()
