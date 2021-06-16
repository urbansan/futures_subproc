import argparse
from pathlib import Path
from .subprocessor import SubProcessor


class Launcher:
    def __init__(self):
        self.parser = self._get_parser()

    def _get_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "filename", type=self._file_exists, help="Filename with commands"
        )
        parser.add_argument(
            "processes",
            type=self._processes_is_int,
            help="Amount of parallel processes",
        )
        return parser

    @staticmethod
    def _processes_is_int(processes):
        try:
            return int(processes)
        except ValueError as er:
            raise argparse.ArgumentTypeError(
                f"Invalid process value '{processes!s}'. Please provide an integer for amount of workers to be used."
            )

    @staticmethod
    def _file_exists(filename: str):
        filepath = Path(filename)
        if not filepath.exists():
            raise argparse.ArgumentTypeError(
                f'File "{filepath.absolute()!s}" does not exist. Please provide an existing file name.'
            )
        else:
            return filepath

    @staticmethod
    def _get_commands(filepath: Path):
        with filepath.open('r') as f:
            cmds = f.readlines()
        return cmds

    def run(self, args=None):
        args = self.parser.parse_args(args)

        cmds = self._get_commands(args.filename)
        processor = SubProcessor(cmds, args.processes)
        processor.run()
