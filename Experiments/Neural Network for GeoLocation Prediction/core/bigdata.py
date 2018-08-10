import consts
import typing
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer


class BigDataFile:

    TEXT_FILE_LINE_SEPARATOR = "\n"
    TEXT_FILE_DATA_SEPARATOR = "\t"
    TEXT_FILE_DATA_SUB_SEPARATOR = ","

    def __init__(self, file : typing.TextIO, feature_dict_size, log_function=None):
        self._file = file
        temp_file = open(file.name, "r", encoding="utf8")

        self._log_function = log_function

        self._encoded_labels = []
        self._file_line_count = 0
        self._feature_count = 0
        self._max_feature_length = 0

        features = []
        labels = []

        self._log("Starting looping through the file...")
        line = temp_file.readline().replace(BigDataFile.TEXT_FILE_LINE_SEPARATOR, "")
        while not line == "":
            try:
                example_feature_set = self._get_features_from_line(line)
                example_label = self._get_label_from_line(line)

                # Making the label lowercase
                example_label = example_label.lower()

                # Check and save the max length of possible features
                for example_feature in example_feature_set:
                    # Adding the feature to the features list.
                    features.append(example_feature)

                    if len(example_feature) > self._max_feature_length:
                        self._max_feature_length = len(example_feature)

                    # Adding the label to labels list
                    labels.append(example_label)

                if example_label not in [example_feature.lower() for example_feature in example_feature_set]:
                    features.append(example_label)

                self._file_line_count += 1
                self._feature_count += len(example_feature_set)

            except:
                pass

            line = temp_file.readline().replace(BigDataFile.TEXT_FILE_LINE_SEPARATOR, "")

        temp_file.close()
        self._log("Ended looping through the file...")

        # Setup the feature tokenizer.
        self._log("Initializing the feature tokenizer...")
        self._feature_dict_size = feature_dict_size
        self._feature_tokenizer = Tokenizer(num_words=feature_dict_size, char_level=False)
        self._feature_tokenizer.fit_on_texts(features)
        self._log("Completed initializing the feature tokenizer...")

        # Releases the memory for features earlier.
        del features

        # Setup the encoded labels.
        # The following has to be done before making the unique label set unique.
        self._log("Initializing the label encoder...")
        self._label_encoder = LabelEncoder()
        self._label_encoder.fit(labels)
        self._encoded_labels = self._label_encoder.transform(labels)
        self._log("Completed initializing the label encoder...")

        # Mapper for transformed label to text label.
        self._log("Populating the label mapper...")
        self._text_labels_for_trans_labels = [None] * len(set(labels))
        for i in range(len(self._encoded_labels)):
            self._text_labels_for_trans_labels[self._encoded_labels[i]] = labels[i]
        self._log("Completed initializing the label mapper.")

        # Making labels contain only the unique labels.
        labels = list(set(labels))
        self._unique_labels_count = len(labels)

        # Releases the memory for labels bit earlier.
        del labels

        self._example_ptr = 0
        self._feature_stack = None

    def _log(self, msg):
        if self._log_function is not None:
            self._log_function(msg)

    def _get_next_line(self):
        return self._file.readline().replace("\n", "")

    def refresh_pointers(self):
        self._file.close()
        self._file = open(self._file.name, "r", encoding="utf8")

        self._example_ptr = 0

    @staticmethod
    def _get_features_from_line(example : str):
        example_col_data = example.split(BigDataFile.TEXT_FILE_DATA_SEPARATOR)
        example_feature_set = example_col_data[consts.TEXT_FILE_COL_INDEX_ALT_NAMES].split(BigDataFile.TEXT_FILE_DATA_SUB_SEPARATOR)
        example_feature_set = list(filter(None, example_feature_set))

        example_label = example_col_data[consts.TEXT_FILE_COL_INDEX_REAL_NAME]
        if example_label not in example_feature_set:
            example_feature_set.append(example_label)

        return example_feature_set

    @staticmethod
    def _get_label_from_line(example : str):
        example_col_data = example.split(BigDataFile.TEXT_FILE_DATA_SEPARATOR)
        example_label = example_col_data[consts.TEXT_FILE_COL_INDEX_REAL_NAME]
        return example_label

    def get_next_example(self):
        label_for_features = self._encoded_labels[self._example_ptr]

        if self._feature_stack is None or len(self._feature_stack) == 0:
            self._feature_stack = []

            line = self._get_next_line()
            if not line == "":
                features_in_line = self._get_features_from_line(line)

                for feature_in_line in features_in_line:
                    self._feature_stack.append(feature_in_line)

            else:
                return None, None

            # Increase the pointer by 1
            self._example_ptr += 1

        return_example_feature = self._feature_stack.pop(0)
        return_example_label = label_for_features
        return return_example_feature, return_example_label

    def get_transformed_labels(self):
        return self._text_labels_for_trans_labels

    def get_unique_labels_count(self):
        return self._unique_labels_count

    def get_file_line_count(self):
        return self._file_line_count

    def get_max_feature_length(self):
        return self._max_feature_length

    def get_feature_count(self):
        return self._feature_count

    def get_feature_dict_size(self):
        return self._feature_dict_size

    def get_feature_tokenizer(self):
        return self._feature_tokenizer
