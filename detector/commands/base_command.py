from argparse import ArgumentParser
from importlib import import_module

from detector.settings import INSTANCE_TYPES


class BaseCommand:
    help = ""

    def add_arguments(self, parser: ArgumentParser):
        pass

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = ArgumentParser(prog=f"{prog_name} {subcommand}", description=self.help or None, **kwargs)
        self.add_arguments(parser)
        return parser

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop("args", ())
        self.execute(*args, **cmd_options)

    def execute(self, *args, **options):
        return self.handle(*args, **options)

    def handle(self, *args, **cmd_options):
        pass

    def get_instance(self, instance_type: str, options: dict, instance_args=[], instance_kwargs={}) -> object:
        instance_settings = INSTANCE_TYPES[instance_type]
        module_name = instance_settings["module"]
        available_classes = instance_settings["classes"]

        instance_name = options[instance_type]
        cls = getattr(import_module(module_name), available_classes[instance_name]["class"])

        instance_args = instance_args + [options.get(key) for key in available_classes[instance_name].get("args", [])]

        return cls(*instance_args, **instance_kwargs)
