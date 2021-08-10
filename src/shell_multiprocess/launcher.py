import argparse
from pathlib import Path


class Launcher:
    def __init__(self):
        self.parser = self._get_parser()

    def get_cmds_and_proc_count(self):
        args = self.parser.parse_args()
        with args.filename.open("r") as f:
            cmds = f.readlines()
        return cmds, args.processes

    def _get_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "filename", type=self._existing_filepath, help="Filename with commands"
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
                f"Invalid process count value '{processes!s}'."
                f" Please provide an integer for amount of workers to be used."
            )

    @staticmethod
    def _existing_filepath(filename: str) -> Path:
        filepath = Path(filename)
        if not filepath.exists():
            raise argparse.ArgumentTypeError(
                f'File "{filepath.absolute()!s}" does not exist. Please provide an existing file name.'
            )
        else:
            return filepath
