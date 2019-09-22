from UniversalModelTrainerProcess.models.geolocations.data.eavesdrop import EavesdropData
from UniversalModelTrainerProcess.models.geolocations.postprocessors.eavesdrop import EavesdropDataPostProcessor
from UniversalModelTrainerProcess.models.geolocations.preprocesses.eavesdrop import EavesdropDataPreProcessor
from commons.universalmodel.geolocations.preferredgeolocations import PreferredGeoLocationsModel


class PreferredGeoLocationsTrainer:

    def __init__(self, processes_abs_folder_path: str, geo_locations_identifier_model_folder_path: str):
        self._processes_abs_folder_path = processes_abs_folder_path
        self._geo_locations_identifier_model_folder_path = geo_locations_identifier_model_folder_path

        self._preferred_geo_locations_model = PreferredGeoLocationsModel(processes_abs_folder_path)

    def _train_using_eavesdrop_data(self):
        eavesdrop_data_handler = EavesdropData(self._processes_abs_folder_path)
        eavesdrop_tracks = eavesdrop_data_handler.get_unused_track_names_for_training()

        eavesdrop_data_pre_processor = EavesdropDataPreProcessor(eavesdrop_tracks, self._geo_locations_identifier_model_folder_path)
        eavesdrop_data_geo_locations_tagged = eavesdrop_data_pre_processor.get_tagged_geo_locations()

        for universal_model_geo_location in eavesdrop_data_geo_locations_tagged:
            if universal_model_geo_location is not None:
                self._preferred_geo_locations_model.add_location(universal_model_geo_location.get_preferred_geo_location())

    def _do_post_processing_eavesdrop_data(self):
        eavesdrop_data_handler = EavesdropData(self._processes_abs_folder_path)
        eavesdrop_data_post_processor = EavesdropDataPostProcessor(eavesdrop_data_handler)
        eavesdrop_data_post_processor.save_processed_file_names()

    def train(self):
        self._train_using_eavesdrop_data()

        # At the end of the training, do post processing.
        self._do_post_processing_eavesdrop_data()
