import speech_recognition as SR
import UniversalModelTrainerProcess.consts.trainers as consts_trainers
import UniversalModelTrainerProcess.models.geolocations.preprocesses.config.eavesdrop as config_trainers_pre_processes_eavesdrop
from keras.models import load_model
import pickle
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from UniversalModelTrainerProcess.models.geolocations.structs.eavesdrop import EavesdropDataGeoLocation


class EavesdropDataPreProcessor:

    def __init__(self, track_files_paths: list, geo_location_model_folder_path: str):
        self._track_files_paths = track_files_paths

        self._speech_recognizer = SR.Recognizer()
        self._locator = load_model(geo_location_model_folder_path + "/" + consts_trainers.EAVESDROP_DATA_PRE_PROCESSOR_GLM_MODEL_FILE_NAME)

        file_processors = open(geo_location_model_folder_path + "/" + consts_trainers.EAVESDROP_DATA_PRE_PROCESSOR_GLM_PROCESSORS_FILE_NAME, "rb")
        _, _, _, _, _, self._text_tokenizer, _, _, _, _, _, self._geo_location_mapper_to_coordinates, _, self._geo_location_names = pickle.load(file_processors)

        file_vars = open(geo_location_model_folder_path + "/" + consts_trainers.EAVESDROP_DATA_PRE_PROCESSOR_GLM_VARS_FILE_NAME, "rb")
        _, _, self._MAX_TEXT_SEQUENCE_LENGTH, _, _ = pickle.load(file_vars)

    def get_read_and_transcribed(self):
        transcriptions = []
        for track_file_path in self._track_files_paths:
            with SR.AudioFile(track_file_path) as track_audio_file:
                try:
                    track_audio_data = self._speech_recognizer.record(track_audio_file)
                    # Use Google Speech recognizer as the master branch is still supposed to use Google APIs
                    track_text_data = self._speech_recognizer.recognize_google(track_audio_data)
                    transcriptions.append(track_text_data)

                except Exception:
                    transcriptions.append("")

        return transcriptions

    def get_tagged_geo_locations(self):
        transcriptions = self.get_read_and_transcribed()
        transcriptions_sequences = []
        for transcription in transcriptions:
            transcription_sequences = pad_sequences(np.asarray(self._text_tokenizer.texts_to_sequences([transcription])), maxlen=self._MAX_TEXT_SEQUENCE_LENGTH)
            transcriptions_sequences.append(transcription_sequences)

        predictions = self._locator.predict(transcriptions_sequences)
        transcription_tags = []
        for transcription_index in range(predictions.shape[0]):
            scores_for_transcription_index = predictions[transcription_index]
            best_location_index_for_transcription = scores_for_transcription_index.argsort()[-1]
            best_score_for_transcription = scores_for_transcription_index[best_location_index_for_transcription]

            if best_score_for_transcription >= config_trainers_pre_processes_eavesdrop.MIN_THRESHOLD_SCORE_FOR_LOCATION:
                # TODO: Maybe a sentiment analysis of entire transcription would provide a intuition about the nuance of the sentence. Do it.
                best_location_code_name = self._geo_location_names[transcription_index]
                best_location_coordinates = self._geo_location_names[best_location_code_name]
                best_location_um_geo_location = EavesdropDataGeoLocation(transcriptions[transcription_index], best_location_code_name, best_location_coordinates[0], best_location_coordinates[1])
            else:
                best_location_um_geo_location = None

            transcription_tags.append(best_location_um_geo_location)

        return transcription_tags
