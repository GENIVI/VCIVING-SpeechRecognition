import consts
from core.preprocessor import PreProcessor
from core.bigdata import BigDataFile
import numpy as np
import time
import pickle

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Embedding, SpatialDropout1D, BatchNormalization, Dropout, LSTM, Dense


class Trainer:

    def __init__(self, big_data_file_path, feature_dict_size, train_verbose=False):
        self._train_verbose = train_verbose

        self._log("Started reading file: " + big_data_file_path)
        file = open(big_data_file_path, "r", encoding="utf8")
        self._big_data_file : BigDataFile = BigDataFile(file, feature_dict_size, log_function=self._log)
        self._log("Ended reading file: " + big_data_file_path)

        self._training_start_time = None
        self._training_end_time = None

        self._ptr_next_batch_begin = 0

        self._model : Sequential = None

    def _log(self, msg):
        if self._train_verbose:
            print(msg)

    def _next_feature_batch(self, batch_size, pre_process=True):
        return_features_batch = []
        return_labels_batch = []

        total_feature_count = self._big_data_file.get_feature_count()
        next_batch_end = self._ptr_next_batch_begin + batch_size

        if next_batch_end >= total_feature_count:
            while self._ptr_next_batch_begin < total_feature_count:
                feature, label = self._big_data_file.get_next_example()
                return_features_batch.append(feature)
                return_labels_batch.append(label)

                self._ptr_next_batch_begin += 1

            self._big_data_file.refresh_pointers()
            self._ptr_next_batch_begin = 0
            next_batch_end -= total_feature_count

        while self._ptr_next_batch_begin < next_batch_end:
            feature, label = self._big_data_file.get_next_example()
            return_features_batch.append(feature)
            return_labels_batch.append(label)

            self._ptr_next_batch_begin += 1

        if pre_process:
            pre_proc = PreProcessor(return_features_batch, self._big_data_file.get_feature_tokenizer())
            pre_proc.process_dataset()

            return_features_batch = pre_proc.get_encoded_features()

        return_labels_batch = np.asarray(return_labels_batch)

        return return_features_batch, return_labels_batch

    def _feature_batch_generator(self, batch_size):
        while True:
            X, Y = self._next_feature_batch(batch_size=batch_size, pre_process=True)

            yield (X, Y)

    def train(self, epochs=100, batch_size=None, iterations=100, dropout_percent=0.2):
        total_feature_count = self._big_data_file.get_feature_count()
        unique_labels_count = self._big_data_file.get_unique_labels_count()

        if batch_size is None:
            batch_size = total_feature_count
            iterations = 1

        self._model = Sequential()

        # Add the layers
        self._model.add(Embedding(self._big_data_file.get_feature_dict_size(), 50))
        self._model.add(SpatialDropout1D(rate=dropout_percent))
        self._model.add(BatchNormalization())
        self._model.add(Dropout(dropout_percent))
        self._model.add(LSTM(units=30))
        self._model.add(BatchNormalization())
        self._model.add(Dropout(dropout_percent, name="location"))
        self._model.add(Dense(unique_labels_count, activation='softmax'))

        self._model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self._log("Training started...")
        self._training_start_time = time.time()
        self._model.fit_generator(generator=self._feature_batch_generator(batch_size=batch_size), steps_per_epoch=iterations, epochs=epochs, verbose=True)
        self._training_end_time = time.time()
        self._log("Training complete. Elapsed Time: " + str(self.get_training_time()))

    def print_train_summary(self):
        self._model.summary()

    def save_model(self, model_savedir_path):
        model_savefile_path = model_savedir_path + "/" + consts.MODEL_SAVEFILE_NAME
        self._log("Writing model file: " + model_savefile_path)
        self._model.save(model_savefile_path)
        self._log("Completed writing model file.")

        classes_savefile_path = model_savedir_path + "/" + consts.CLASSES_SAVEFILE_NAME
        self._log("Dumping encoded classes file: " + classes_savefile_path)
        with open(classes_savefile_path, "wb") as savefile_classes:
            pickle.dump(self._big_data_file.get_transformed_labels(), savefile_classes, protocol=4)

        self._log("Completed dumping encoded classes file...")

        tokenizer_savefile_path = model_savedir_path + "/" + consts.TOKENIZER_SAVEFILE_NAME
        self._log("Dumping the tokenizer file: " + tokenizer_savefile_path)
        with open(tokenizer_savefile_path, "wb") as savefile_tokenizer:
            pickle.dump(self._big_data_file.get_feature_tokenizer(), savefile_tokenizer, protocol=4)

    def get_training_time(self):
        return self._training_end_time - self._training_start_time
