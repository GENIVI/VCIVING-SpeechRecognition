from UniversalModelTrainerProcess.models.geolocations.data.eavesdrop import EavesdropData


class EavesdropDataPostProcessor:

    # The track_files_names should be just the file names NOT the absolute path to the files.
    def __init__(self, eavesdrop_data_handler: EavesdropData):
        self._eavesdrop_data_handler: EavesdropData = eavesdrop_data_handler

    def save_processed_file_names(self):
        eavesdrop_unused_track_names = self._eavesdrop_data_handler.get_unused_track_names_for_training(return_abs_paths=False)
        eavesdrop_track_use_state = self._eavesdrop_data_handler.get_tracks_marked(eavesdrop_unused_track_names)

        for track_name, track_found_in_db in eavesdrop_track_use_state.items():
            if not track_found_in_db:
                self._eavesdrop_data_handler.mark_as_used_track(track_name)
