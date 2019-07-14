from speech_interpreter import consts
from statistics import mean
from emucorebrain.core.predictor import Predictor
from . import file_reader

_test_data_filepath = consts.DATA_DIR_PATH + "/test_data.json"
_prediction_threshold = 0.2

predictor = Predictor(model_filepath=consts.MODEL_SAVEFILE_PATH, prediction_threshold=_prediction_threshold)

test_sentences, expected_labels = file_reader.read_file_as_dataset(_test_data_filepath)

print("Prediction started.")
prediction_status = [0] * len(test_sentences)
for i in range(len(test_sentences)):
    test_sentence = test_sentences[i]
    expected_label = expected_labels[i]

    predicted_label = predictor.predict_sentence(test_sentence)
    if predicted_label == expected_label:
        prediction_status[i] = 1

    print("Sentence: " + test_sentence + "\t" + "| Expected Label: " + expected_label + "\t" + "| Predicted Label: " + predicted_label)

print("Prediction ended.")

accuracy = mean(prediction_status)
print("Accuracy: " + str(accuracy))
