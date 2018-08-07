import sys, os

sys.path.append(os.path.abspath("."))

from core.predictor import Predictor
import consts

model_folder_path = consts.MODEL_DIR_PATH
predictor = Predictor(model_folder_path)

locations_to_predict = ["mill pond dam", ""]

for location in locations_to_predict:
    predictor.predict_location(location)
