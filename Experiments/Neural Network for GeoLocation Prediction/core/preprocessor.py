from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences


class PreProcessor:

    def __init__(self, text_features, feature_tokenizer : Tokenizer):
        self._text_features = text_features

        self._feature_tokenizer = feature_tokenizer

        self._features = []
        self._labels = []

    def _lowercase_text_features(self):
        for i in range(len(self._text_features)):
            self._text_features[i] = self._text_features[i].lower()

    def _dictionary_encode_features(self):
        self._features = self._feature_tokenizer.texts_to_sequences(self._text_features)
        self._features = np.asarray(self._features)
        self._features = pad_sequences(self._features)

    def process_dataset(self):
        self._lowercase_text_features()
        self._dictionary_encode_features()
        # Labels have already been encoded by big_data_file

    def get_encoded_features(self):
        return self._features

    def get_encoded_labels(self):
        return self._labels

    def get_feature_tokenizer(self):
        return self._feature_tokenizer
