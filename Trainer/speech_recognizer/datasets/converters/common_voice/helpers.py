import os
import sys
from pathlib import Path
import subprocess
import pandas as pd
from speech_recognizer.datasets.converters.common_voice.consts.dataset import TSV_FILE_EXTENSION


def read_tsv(dataset_dir, variant_to_read):
    tsv_file_path = dataset_dir + "/" + variant_to_read + "." + TSV_FILE_EXTENSION
    return pd.read_csv(tsv_file_path, delimiter='\t', encoding="utf-8")


def dir_exists(folder_dir):
    return Path(folder_dir).is_dir()


def check_dirs(*args, print_if_false=True, exit_if_false=False):
    for path_dir in args:
        if not dir_exists(path_dir):
            if print_if_false:
                print("Directory: " + path_dir + " does not exist.")

            if exit_if_false:
                sys.exit()
            else:
                return False

    return True


def file_exists(file_dir):
    return Path(file_dir).is_file()


def delete_file_if_exists(file_dir):
    if file_exists(file_dir):
        os.remove(file_dir)


def get_processed_transcription(transcription: str):
    return transcription.\
        replace("!", "").\
        replace(",", "").\
        replace(";", "").\
        replace(":", "").\
        replace("/", "").\
        replace("\\", "").\
        replace("?", "").\
        replace("\"", "").\
        replace(". ", " ").\
        replace(" '", " ")


def convert_to_wave_file(abs_input_audio_file_path: str, abs_output_audio_file_path: str, output_sampling_rate: int, output_channels: int, output_bit_rate: int):
    return subprocess.run(["sox", abs_input_audio_file_path, "-r", str(output_sampling_rate), "-c", str(output_channels), "-b", str(output_bit_rate), abs_output_audio_file_path])
