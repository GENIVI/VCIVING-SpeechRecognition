from UniversalModelTrainerProcess.models.geolocations.variants.preferredgeolocations import PreferredGeoLocationsTrainer


class GeoLocationsTrainer:

    def __init__(self, processes_abs_folder_path: str, geo_locations_identifier_model_folder_path: str):
        self._preferred_geo_locations_trainer: PreferredGeoLocationsTrainer = PreferredGeoLocationsTrainer(processes_abs_folder_path, geo_locations_identifier_model_folder_path)

    def _train_preferred_geo_locations_model(self):
        self._preferred_geo_locations_trainer.train()

    def train_all(self):
        self._train_preferred_geo_locations_model()
