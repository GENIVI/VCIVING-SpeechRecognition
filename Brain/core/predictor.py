import json
import numpy as np
import keywords.model
from core.preprocessor import PreProcessor
from train.trainer import Trainer


class Predictor:

    def __init__(self, model_filepath, prediction_threshold):
        with open(model_filepath, "r") as model_file:
            model_json = json.load(model_file)

            self._classes = model_json[keywords.model.save_file_classes]
            self._word_list = model_json[keywords.model.save_file_words]
            self._synapse0 = np.asarray(model_json[keywords.model.save_file_synapse0])
            self._synapse1 = np.asarray(model_json[keywords.model.save_file_synapse1])

        self._prediction_threshold = prediction_threshold

    def set_prediction_threshold(self, prediction_threshold):
        self._prediction_threshold = prediction_threshold

    def get_probable_classes_sentence(self, sentence):
        patternized_sentence = PreProcessor.get_sentence_patterns(sentence.lower(), self._word_list)

        # Input layer
        layer0 = patternized_sentence
        # Layer 1
        layer1 = Trainer.sigmoid(np.dot(layer0, self._synapse0))
        # Output layer
        layer2 = Trainer.sigmoid(np.dot(layer1, self._synapse1))

        results = [[i, probability] for i, probability in enumerate(layer2) if probability > self._prediction_threshold]
        results.sort(key=lambda x: x[1], reverse=True)
        return_results = [[self._classes[result[0]], result[1]] for result in results]

        return return_results

    def predict_sentence(self, sentence):
        probabilities = self.get_probable_classes_sentence(sentence)

        max_class = ""
        max_prob = 0

        for probability in probabilities:
            prob_class = probability[0]
            prob = probability[1]

            if prob > max_prob:
                max_class = prob_class
                max_prob = prob

        return max_class
