import consts
import pickle
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


class Predictor:

    def __init__(self, model_folder_path):
        model_file_path = model_folder_path + "/" + consts.MODEL_SAVEFILE_NAME
        self._model = load_model(model_file_path)

        classes_file_path = model_folder_path + "/" + consts.CLASSES_SAVEFILE_NAME
        classes_file = open(classes_file_path, "rb")
        self._classes = pickle.load(classes_file)

        tokenizer_file_path = model_folder_path + "/" + consts.TOKENIZER_SAVEFILE_NAME
        tokenizer_file = open(tokenizer_file_path, "rb")
        self._tokenizer : Tokenizer = pickle.load(tokenizer_file)

    def get_probable_classes(self, location):
        location_seq = self._tokenizer.texts_to_sequences([location])
        location_seq = np.asarray(location_seq)
        location_seq = pad_sequences(location_seq)

        return self._model.predict(location_seq)

    def get_max_probable_classes(self, location):
        predictions = self.get_probable_classes(location)

        top_text_predictions = []
        for index in reversed(predictions.argsort()[0]):
            top_text_predictions.append(self._classes[index])

        return top_text_predictions

    def predict_location(self, location):
        print(self.get_max_probable_classes(location))
