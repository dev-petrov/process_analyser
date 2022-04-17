from IPython import start_ipython

from .base_command import BaseCommand


class ShellCommand(BaseCommand):
    description = "IPython shell"

    def handle(self, *args, **options):
        start_ipython(argv=[])
