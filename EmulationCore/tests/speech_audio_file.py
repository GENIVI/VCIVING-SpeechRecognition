from emucorebrain.data.containers.settings import SettingsContainer
import base.consts.consts as emucore_consts
import os
import speech_recognition as SR
from fuzzywuzzy import fuzz

import tests.utils.args_utils as args_utils

ARG_AUDIO_FILE = "audio_file"
ARG_AUDIO_FILE_TEXT = "text"
ARGUMENTS = {
    ARG_AUDIO_FILE: "The audio file containing speech to be recognized. Must be in wave(.wav) format",
    ARG_AUDIO_FILE_TEXT: "The textual data of the speech in the audio file."
}
args_keys_list = [arg_key for arg_key, _ in ARGUMENTS.items()]
args_utils.add_cli_args(ARGUMENTS)
args_exist_status = args_utils.check_cli_args(args_keys_list)
args_values = args_utils.get_cli_args(args_keys_list)

ivi_settings = SettingsContainer(emucore_consts.SETTINGS_FILEPATH)

if args_exist_status[ARG_AUDIO_FILE_TEXT]:
    if args_exist_status[ARG_AUDIO_FILE]:
        speech_audio_file_path = os.path.abspath(args_values[ARG_AUDIO_FILE])
        if os.path.exists(speech_audio_file_path):
            recognizer = SR.Recognizer()
            with SR.AudioFile(speech_audio_file_path) as source:
                audio = recognizer.record(source)

            try:
                recognized_text = recognizer.recognize_google(audio)

                print("Transcribed Text: " + recognized_text)
                print("Expected Text: " + args_values[ARG_AUDIO_FILE_TEXT])

                score = fuzz.ratio(recognized_text, args_values[ARG_AUDIO_FILE_TEXT])
                print("Fuzz Score: " + str(score))

            except SR.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except SR.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    else:
        print("Please provide a file to perform speech recognition. Use --" + ARG_AUDIO_FILE + " option.")
else:
    print("Comparison text not found. Use --" + ARG_AUDIO_FILE_TEXT + " option.")
