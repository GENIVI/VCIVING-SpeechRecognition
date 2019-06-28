from emucorebrain.data.containers.settings import SettingsContainer
import base.consts.consts as emucore_consts
import os
import speech_recognition as SR

import tests.utils.args_utils as args_utils
import tests.utils.str_utils as str_utils

ACCEPTED_AUDIO_FORMATS = ["wav", "flac"]
ACCEPTED_TRANSCRIPTION_FORMAT = "txt"

ARG_AUDIO_FILE = "audio_file"
ARG_AUDIO_DIR = "audio_dir"
ARG_AUDIO_FILE_TEXT = "text"
ARGUMENTS = {
    ARG_AUDIO_FILE: "The audio file containing speech to be recognized. Must be in one of the following formats: " + ",".join(ACCEPTED_AUDIO_FORMATS),
    ARG_AUDIO_DIR: "The directory containing audio files and the transcriptions of them with the same file name(as of audio file) under ." + ACCEPTED_TRANSCRIPTION_FORMAT + " format",
    ARG_AUDIO_FILE_TEXT: "The textual data of the speech in the audio file."
}
args_keys_list = [arg_key for arg_key, _ in ARGUMENTS.items()]
args_utils.add_optional_cli_args(ARGUMENTS)
args_exist_status = args_utils.check_cli_args(args_keys_list)
args_values = args_utils.get_cli_args(args_keys_list)

ivi_settings = SettingsContainer(emucore_consts.SETTINGS_FILEPATH)

def perform_recognition(audio_file_path, expected_text):
    recognizer = SR.Recognizer()
    with SR.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        print("Expected Text: " + expected_text)
        print("Speech Recognition in Process...")
        recognized_text = recognizer.recognize_google(audio)
        print("Speech Recognition Completed...")
        print("Transcribed Text: " + recognized_text)

        score = str_utils.match_percentage(recognized_text, expected_text)
        print("Accuracy Percentage: " + str(score))

    except SR.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except SR.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if args_exist_status[ARG_AUDIO_FILE] and args_exist_status[ARG_AUDIO_FILE_TEXT] and not args_exist_status[ARG_AUDIO_DIR]:
    speech_audio_file_path = os.path.abspath(args_values[ARG_AUDIO_FILE])
    if os.path.exists(speech_audio_file_path):
        perform_recognition(speech_audio_file_path, args_values[ARG_AUDIO_FILE_TEXT])
    else:
        print("The given audio file does not exist.")
elif not args_exist_status[ARG_AUDIO_FILE] and not args_exist_status[ARG_AUDIO_FILE_TEXT] and args_exist_status[ARG_AUDIO_DIR]:
    audio_dir_folder_path = os.path.abspath(args_values[ARG_AUDIO_DIR])

    if os.path.isdir(audio_dir_folder_path):
        all_audio_dir_file_names = os.listdir(audio_dir_folder_path)
        audio_file_names = [file_name for file_name in all_audio_dir_file_names if os.path.splitext(file_name)[1].replace(".", "") in ACCEPTED_AUDIO_FORMATS]

        if len(audio_file_names) > 0:
            all_transc_exists = True
            for audio_file_name in audio_file_names:
                if not all_transc_exists:
                    break

                audio_transcription_file_name = os.path.splitext(audio_file_name)[0] + "." + ACCEPTED_TRANSCRIPTION_FORMAT
                audio_transcription_file_path = audio_dir_folder_path + "/" + audio_transcription_file_name
                all_transc_exists = os.path.exists(audio_transcription_file_path)

            if all_transc_exists:
                print("Directory OK. Starting...")
                for audio_file_name in audio_file_names:
                    print("Recognition on: " + audio_file_name)

                    audio_file_path = audio_dir_folder_path + "/" + audio_file_name

                    print("Reading Transcription File...")
                    audio_transcription_file_path = audio_dir_folder_path + "/" + os.path.splitext(audio_file_name)[0] + "." + ACCEPTED_TRANSCRIPTION_FORMAT
                    audio_transcription_file = open(audio_transcription_file_path, "r")
                    audio_transcription = audio_transcription_file.read().strip()
                    print("Completed Reading Transcription File...")

                    print("==================================================")
                    print("Speech Recognition for File: " + audio_file_name)
                    perform_recognition(audio_file_path, audio_transcription)
                    print("Speech Recognition Completed for File: " + audio_file_name)
                    print("==================================================")

                    print("**************************************************")

                print("Directory Completed.")
            else:
                print("Not all the audio files have their transcriptions files together inside in the given directory. Please re-check the directory.")
        else:
            print("The provided directory does not contain any valid audio files.")
else:
    print("Please re-check the combination of the arguments you've used.")
