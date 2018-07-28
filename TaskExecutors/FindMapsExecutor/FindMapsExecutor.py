from emucorebrain.data.abstracts.TaskExecutor import TaskExecutor
import emucorebrain.keywords.task_executor as keywords_task_executor
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
from emucorebrain.data.carriers.string import StringCarrier
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from FindMapsExecutor.db.predictor import Predictor

# Temporarily used to open the Google Maps with the latitudes and longitudes
import webbrowser


class FindMapsExecutor(TaskExecutor):

    DATABASE_COL_INDEX_REAL_NAME = 1
    DATABASE_COL_INDEX_ALT_NAMES = 3
    DATABASE_COL_INDEX_GEO_LAT = 4
    DATABASE_COL_INDEX_GEO_LONG = 5

    SETTING_LOCATION_DB_NAMES_FILEPATH_KEY = "db_location_names_filepath"
    SETTING_LOCATION_DB_MAPPERS_FILEPATH_KEY = "db_location_mapper_filepath"

    def __init__(self):
        pass

    # Executes the negative run method of FindMapsExecutor.
    def run_negative(self, args):
        pass

    # Executes the FindMapsExecutor.
    # The main method executed when prediction is directed to this class.
    def run(self, args):
        data : StringCarrier = args[keywords_task_executor.ARG_SPEECH_TEXT_DATA]
        ivi_settings: SettingsContainer = args[keywords_task_executor.ARG_SETTINGS_CONTAINER]
        ivi_outs_mechanisms_carriers = args[keywords_task_executor.ARG_OUTS_MECHANISMS_CARRIERS]
        ivi_outs_mechanism_carrier_default: OutputMechanismCarrier = ivi_outs_mechanisms_carriers[keywords_task_executor.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT]
        ivi_outs_mechanism_default: OutputMechanism = ivi_outs_mechanism_carrier_default.get_data()

        ivi_outs_mechanism_default.write_data("Please wait while we look for the location for you.", wait_until_completed=True)
        db_location_filepath = ivi_settings.get_setting(FindMapsExecutor.SETTING_LOCATION_DB_NAMES_FILEPATH_KEY)
        db_mapper_filepath = ivi_settings.get_setting(FindMapsExecutor.SETTING_LOCATION_DB_MAPPERS_FILEPATH_KEY)
        predictor = Predictor(db_location_filepath, db_mapper_filepath)

        location_name, geo_latitude, geo_longitude = predictor.get_geo_location_for_phrase(data.get_data(), return_location_name=True)
        if location_name is not None:
            ivi_outs_mechanism_default.write_data("The location you've requested seems to be " + location_name + ". We'll open it up in Google Maps.", wait_until_completed=True)
            if geo_latitude is not None and geo_longitude is not None:
                gmaps_url = "https://maps.google.com/?q=" + geo_latitude + "," + geo_longitude
            else:
                ivi_outs_mechanism_default.write_data("We could not find the geological data for the location you've requested. We'll try with the location name.", wait_until_completed=True)
                gmaps_url = "https://maps.google.com/?q=" + location_name

            webbrowser.open(gmaps_url)
        else:
            ivi_outs_mechanism_default.write_data("We could not find such a place. We're extremely sorry.", wait_until_completed=True)

