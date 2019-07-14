import argparse


def get_cli_args(args_help_dict: dict):
    parser = argparse.ArgumentParser()

    for arg, help_str in args_help_dict.items():
        parser.add_argument("--" + arg, help=help_str, required=True)

    return vars(parser.parse_args())
