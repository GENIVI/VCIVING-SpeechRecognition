import argparse

def get_cli_args(arg_keys: list):
    parser = argparse.ArgumentParser()

    for arg_key in arg_keys:
        parser.add_argument("--" + arg_key)

    return vars(parser.parse_args())

def check_cli_args(check_arg_keys: list):
    dict_args = get_cli_args(check_arg_keys)
    exist_dict = {}
    for arg in check_arg_keys:
        exist_dict[arg] = dict_args[arg] is not None

    return exist_dict

def add_cli_args(args_help_dict: dict):
    parser = argparse.ArgumentParser()

    for arg, help_str in args_help_dict.items():
        parser.add_argument(arg, help=help_str)
