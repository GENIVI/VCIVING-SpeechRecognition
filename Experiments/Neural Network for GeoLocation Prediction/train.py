import sys, os

sys.path.append(os.path.abspath("."))

import consts
from core.trainer import Trainer

_train_data_filepath = consts.DATA_DIR_PATH + "/US.txt"
_train_model_save_folderpath = consts.MODEL_DIR_PATH

_training_feature_dict_size = 100000
_training_process_verbose = True
_training_epochs = 1
_training_batch_size = 128
_training_iterations = 14000
_training_dropout_percent = 0.2

trainer = Trainer(big_data_file_path=_train_data_filepath, train_verbose=_training_process_verbose, feature_dict_size=_training_feature_dict_size)
trainer.train(epochs=_training_epochs, batch_size=_training_batch_size, iterations=_training_iterations, dropout_percent=_training_dropout_percent)
trainer.save_model(_train_model_save_folderpath)
print("Training completed successfully.")
