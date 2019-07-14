import sys, os
sys.path.append(os.path.abspath("../../../"))

import pandas as pd
import speech_recognizer.utils.args_utils as arg_utils
from pathlib import Path
import subprocess

# Following values are constants and cannot be changed.
TSV_FILE_EXTENSION = "tsv"
AUDIO_FILES_SUBDIR = "clips"
OUTPUT_AUDIO_FORMAT = "wav"
OUTPUT_AUDIO_SAMPLING_RATE = 16000
OUTPUT_AUDIO_CHANNELS = 1
OUTPUT_AUDIO_BITRATE = 16

TSV_COLUMN_NAME_FILE_NAME = "path"
TSV_COLUMN_NAME_TRANSCRIPTION = "sentence"

OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT = "variant"
OUTPUT_FILE_NAME_FIELDS = "common_voice_" + OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT + ".fields"
OUTPUT_FILE_NAME_TRANSCRIPTION = "common_voice_" + OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT + ".transcription"

ARG_DATASET_DIR = "dataset_dir"
ARG_OUTPUT_DIR = "output_dir"
ARG_VARIANT = "variant"
ARGUMENTS = {
    ARG_DATASET_DIR: "The absolute path to the directory containing the dataset.",
    ARG_OUTPUT_DIR: "The absolute path to the directory where the CMUSphinx dataset should be created.",
    ARG_VARIANT: "The variant of the dataset to be read.(invalidated/validated/dev/test/train..)"
}
# End of the constants that cannot be changed.

# Function definitions


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

# End of Function Definitions

# Procedure


cli_args = arg_utils.get_cli_args(ARGUMENTS)
arg_dataset_dir = cli_args[ARG_DATASET_DIR]
arg_output_dir = cli_args[ARG_OUTPUT_DIR]
dataset_variant_to_read = cli_args[ARG_VARIANT]

# Creates the variables required for other directories.
audio_files_dataset_dir = arg_dataset_dir + "/" + AUDIO_FILES_SUBDIR

# Checks for the directories
check_dirs(arg_dataset_dir, audio_files_dataset_dir, arg_output_dir, print_if_false=True, exit_if_false=True)

print("Reading the dataset...")
dataset = read_tsv(arg_dataset_dir, dataset_variant_to_read)

# Preparing output directory as a CMUSphinx Compatible model
print("Reading the required files...")
abs_path_fields_file = arg_output_dir + "/" + OUTPUT_FILE_NAME_FIELDS.replace(OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT, dataset_variant_to_read)
abs_path_transcription_file = arg_output_dir + "/" + OUTPUT_FILE_NAME_TRANSCRIPTION.replace(OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT, dataset_variant_to_read)
delete_file_if_exists(abs_path_fields_file)
delete_file_if_exists(abs_path_transcription_file)
output_file_fields = open(abs_path_fields_file, "w+")
output_file_transcription = open(abs_path_transcription_file, "w+")

# Iterating through the files and converting each one
print("Started Iterating Dataset...")
for audio_file_index, entry in dataset.iterrows():
    audio_file_name = entry[TSV_COLUMN_NAME_FILE_NAME]
    audio_file_identifier, _ = os.path.splitext(audio_file_name)
    audio_file_transcription = entry[TSV_COLUMN_NAME_TRANSCRIPTION]

    # Skip missing transcriptions.
    if audio_file_transcription != "":
        print("Reading Index: " + str(audio_file_index) + "; File Name: " + audio_file_name + ";")

        abs_path_audio_file_input = audio_files_dataset_dir + "/" + audio_file_name
        abs_path_audio_file_output = arg_output_dir + "/" + audio_file_identifier + "." + OUTPUT_AUDIO_FORMAT
        print("Attempting to convert the audio file...")
        conversion_process = subprocess.run(["sox", abs_path_audio_file_input, "-r", str(OUTPUT_AUDIO_SAMPLING_RATE), "-c", str(OUTPUT_AUDIO_CHANNELS), "-b", str(OUTPUT_AUDIO_BITRATE), abs_path_audio_file_output])
        if conversion_process.returncode == 0:
            print("Audio file conversion Successful.")

            try:
                print("Adding File Name to Fields file...")
                output_file_fields.write(audio_file_identifier + "\n")
                print("Successfully added File Name to Fields File.")

            except:
                print("Unexpected exception while writing to fields file. Skipping...")

                # Deleting the audio file converted
                os.remove(abs_path_audio_file_output)

            try:
                print("Copying Transcription...")
                output_file_transcription.write("<s> " + audio_file_transcription + " </s> (" + audio_file_identifier + ")\n")
                print("Successfully Copied Transcription.")

            except:
                print("Unexpected exception while writing to transcriptions file. Skipping...")

                # Removing the line written to fields file.
                fields_file_content_valid = output_file_fields.readlines()[:-1]
                output_file_fields.truncate()
                output_file_fields.writelines(fields_file_content_valid)

                # Deleting the audio file converted
                os.remove(abs_path_audio_file_output)

            print("Finished Processing Index: " + str(audio_file_index) + "; Audio File: " + audio_file_name + ";")
        else:
            print("Audio file conversion failed, Skipping...")
    else:
        print("Skipping Index: " + str(audio_file_index) + "; Audio File: " + audio_file_name + "; due to missing transcription")

print("Closing down file streams...")
output_file_fields.close()
output_file_transcription.close()
print("Successfully closed down file streams.")

print("Dataset Conversion Completed.")
