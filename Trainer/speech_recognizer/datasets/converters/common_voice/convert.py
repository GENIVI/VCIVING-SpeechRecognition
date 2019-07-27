import sys, os
sys.path.append(os.path.abspath("../../../../"))
import speech_recognizer.datasets.converters.common_voice.config as config
import speech_recognizer.datasets.converters.common_voice.consts.cli as cli
import speech_recognizer.datasets.converters.common_voice.consts.output as consts_output
import speech_recognizer.datasets.converters.common_voice.consts.dataset as consts_dataset
import speech_recognizer.datasets.converters.common_voice.helpers as helpers
import speech_recognizer.utils.args_utils as arg_utils

cli_args = arg_utils.get_cli_args(cli.ARGUMENTS)
arg_dataset_dir = cli_args[cli.ARG_DATASET_DIR]
arg_output_dir = cli_args[cli.ARG_OUTPUT_DIR]
dataset_variant_to_read = cli_args[cli.ARG_VARIANT]

# Creates the variables required for other directories.
audio_files_dataset_dir = arg_dataset_dir + "/" + consts_dataset.AUDIO_FILES_SUBDIR
# Checks for the directories
helpers.check_dirs(arg_dataset_dir, audio_files_dataset_dir, arg_output_dir, print_if_false=True, exit_if_false=True)

print("Reading the dataset...")
dataset = helpers.read_tsv(arg_dataset_dir, dataset_variant_to_read)

# Preparing output directory as a CMUSphinx Compatible model
print("Reading the required files...")
abs_path_fields_file = arg_output_dir + "/" + config.OUTPUT_FILE_NAME_FIELDS.replace(config.OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT, dataset_variant_to_read)
abs_path_transcription_file = arg_output_dir + "/" + config.OUTPUT_FILE_NAME_TRANSCRIPTION.replace(config.OUTPUT_FILE_NAME_PLACEHOLDER_VARIANT, dataset_variant_to_read)
helpers.delete_file_if_exists(abs_path_fields_file)
helpers.delete_file_if_exists(abs_path_transcription_file)
output_file_fields = open(abs_path_fields_file, "w+")
output_file_transcription = open(abs_path_transcription_file, "w+")

# Iterating through the files and converting each one
print("Started Iterating Dataset...")
for audio_file_index, entry in dataset.iterrows():
    audio_file_name = entry[consts_dataset.TSV_COLUMN_NAME_FILE_NAME]
    audio_file_identifier, _ = os.path.splitext(audio_file_name)
    audio_file_transcription: str = helpers.get_processed_transcription(entry[consts_dataset.TSV_COLUMN_NAME_TRANSCRIPTION])

    # Skip missing transcriptions.
    if audio_file_transcription != "":
        print("Reading Index: " + str(audio_file_index) + "; File Name: " + audio_file_name + ";")

        abs_path_audio_file_input = audio_files_dataset_dir + "/" + audio_file_name
        abs_path_audio_file_output = arg_output_dir + "/" + audio_file_identifier + "." + consts_output.OUTPUT_AUDIO_FORMAT
        print("Attempting to convert the audio file...")
        conversion_process = helpers.convert_to_wave_file(abs_path_audio_file_input, abs_path_audio_file_output, consts_output.OUTPUT_AUDIO_SAMPLING_RATE, consts_output.OUTPUT_AUDIO_CHANNELS, consts_output.OUTPUT_AUDIO_BITRATE)
        if conversion_process.returncode == 0 and helpers.file_exists(abs_path_audio_file_output):
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
