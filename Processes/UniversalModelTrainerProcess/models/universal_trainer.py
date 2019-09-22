from emucorebrain.data.containers.settings import SettingsContainer
from UniversalModelTrainerProcess.models.geolocations.geolocationstrainer import GeoLocationsTrainer
import commons.keywords.settings as common_keywords_settings
import commons.locations.keywords.settings as locations_keywords_settings

_trainer_geo_locations: GeoLocationsTrainer = None


def init_trainers(ivi_settings: SettingsContainer):
    global _trainer_geo_locations

    # Init GeoLocationsTrainer
    processes_abs_folder_path: str = ivi_settings.get_setting(common_keywords_settings.ARG_PROCESSES_FOLDER_PATH)
    geo_locations_identifier_model_folder_path: str = ivi_settings.get_setting(locations_keywords_settings.ARG_LOCATION_TAGGER_MODEL_FOLDER_PATH)
    _trainer_geo_locations = GeoLocationsTrainer(processes_abs_folder_path, geo_locations_identifier_model_folder_path)

    # TODO: Init other trainers here.


def run_trainers():
    # Run Geo Locations trainer.
    _trainer_geo_locations.train_all()

    # TODO: Run other trainers here.
