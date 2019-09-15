import os
import EavesdropProcess.consts.recordings as consts_recordings
import commons.eavesdrop.consts.dirs


def convert_save_folder_to_eaves_folder(save_folder_path: str):
    abs_save_folder_path = os.path.abspath(save_folder_path)
    if not os.path.isdir(abs_save_folder_path):
        os.makedirs(abs_save_folder_path)

    abs_save_audio_folder_path = abs_save_folder_path + "/" + commons.eavesdrop.consts.dirs.SAVE_FOLDER_SUB_DIR_AUDIO_FILES
    if not os.path.isdir(abs_save_audio_folder_path):
        os.makedirs(abs_save_audio_folder_path)

    abs_save_transcriptions_folder_path = abs_save_folder_path + "/" + commons.eavesdrop.consts.dirs.SAVE_FOLDER_SUB_DIR_TRANSCRIPTIONS
    if not os.path.isdir(abs_save_transcriptions_folder_path):
        os.makedirs(abs_save_transcriptions_folder_path)


def get_audio_file_names(eaves_folder_path, start_time, end_time):
    str_start_time = str(start_time).split('.')[0]
    str_end_time = str(end_time).split('.')[0]

    abs_audio_file_path = eaves_folder_path + "/" + commons.eavesdrop.consts.dirs.SAVE_FOLDER_SUB_DIR_AUDIO_FILES + "/" + str_start_time + "_" + str_end_time + "." + consts_recordings.AUDIO_FILE_FORMAT
    abs_transcription_file_path = eaves_folder_path + "/" + commons.eavesdrop.consts.dirs.SAVE_FOLDER_SUB_DIR_TRANSCRIPTIONS + "/" + str_start_time + "_" + str_end_time + "." + consts_recordings.TRANSCRIPTION_FILE_FORMAT

    return abs_audio_file_path, abs_transcription_file_path
