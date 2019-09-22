import UniversalModelTrainerProcess.config.trainers as config_trainers
import commons.eavesdrop.config.dirs
import commons.eavesdrop.consts.dirs as consts_eavesdrop_dirs
import os


class EavesdropData:

    def __init__(self, processes_abs_folder_path: str):
        self._eavesdrop_data_folder_path = processes_abs_folder_path + "/" + commons.eavesdrop.config.dirs.SAVE_FOLDER_DIR
        self._eavesdrop_data_used_files_db_file_path = processes_abs_folder_path + "/UniversalModelTrainerProcess/" + config_trainers.EAVESDROP_USED_FILES_DATA_DB_FILE_PATH

        # Create db file if it does not exist.
        if not os.path.isfile(self._eavesdrop_data_used_files_db_file_path):
            temp_used_file_db = open(self._eavesdrop_data_used_files_db_file_path, "w+")
            temp_used_file_db.close()

    def get_unused_track_names_for_training(self, return_abs_paths=True):
        eavesdrop_clips_data_folder_path = self._eavesdrop_data_folder_path + "/" + consts_eavesdrop_dirs.SAVE_FOLDER_SUB_DIR_AUDIO_FILES
        eavesdrop_all_clips_file_names = os.listdir(eavesdrop_clips_data_folder_path)

        eavesdrop_unused_clips_file_names = []
        with open(self._eavesdrop_data_used_files_db_file_path, "r") as used_file_db:
            for eavesdrop_clip_file_name in eavesdrop_all_clips_file_names:
                eavesdrop_clip_file_used = False
                for used_file_name in used_file_db:
                    if eavesdrop_clip_file_name == used_file_name:
                        eavesdrop_clip_file_used = True
                        break
                used_file_db.seek(0)

                if not eavesdrop_clip_file_used:
                    if return_abs_paths:
                        eavesdrop_unused_clips_file_names.append(eavesdrop_clips_data_folder_path + "/" + eavesdrop_clip_file_name)
                    else:
                        eavesdrop_unused_clips_file_names.append(eavesdrop_clip_file_name)

        used_file_db.close()

        return eavesdrop_unused_clips_file_names

    # Returns a dictionary containing values for each track name indicating whether they are found in database. (by True or False).
    def get_tracks_marked(self, track_files_names: list):
        with open(self._eavesdrop_data_used_files_db_file_path, "r") as used_file_db:
            track_files_names_existence = dict.fromkeys(track_files_names, False)
            for used_file_name in used_file_db:
                if used_file_name in track_files_names:
                    track_files_names_existence[used_file_name] = True

            used_file_db.close()

            return track_files_names_existence

    def mark_as_used_track(self, track_file_name: str):
        with open(self._eavesdrop_data_used_files_db_file_path, "a") as used_db_file:
            used_db_file.writelines(track_file_name + "\n")
