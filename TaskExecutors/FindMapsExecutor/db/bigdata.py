import FindMapsExecutor.db.consts as consts


class BigDataFile:

    TEXT_FILE_LINE_SEPARATOR = "\n"
    TEXT_FILE_DATA_SEPARATOR = "\t"
    TEXT_FILE_DATA_SUB_SEPARATOR = ","

    EXAMPLE_SET_KEY_FEATURE = "feature"
    EXAMPLE_SET_KEY_LABEL = "label"
    EXAMPLE_SET_KEY_LOCATION = "location"

    def __init__(self, file_path : str, log_function=None, batch_size=1):
        self._file = self._open_big_data_file(file_path)
        self._log_function = log_function
        self._batch_size = batch_size

        self._file_line_count = 0

        features = []
        labels = []

        self._log("Starting looping through the file...")
        temp_file = self._open_big_data_file(self._file.name)
        line = temp_file.readline().replace(BigDataFile.TEXT_FILE_LINE_SEPARATOR, "")
        while not line == "":
            try:
                self._file_line_count += 1

                features_in_line = self._get_features_from_line(line)
                features.extend(features_in_line)

                label_for_line = self._get_label_from_line(line)
                labels.append(label_for_line)

            except:
                pass

            line = temp_file.readline().replace(BigDataFile.TEXT_FILE_LINE_SEPARATOR, "")

        temp_file.close()
        self._log("Ended looping through the file...")

        # Counting the number of features
        self._example_count = len(features)
        # Removes features from memory.
        del features

        # Making labels contain only the unique labels.
        labels = list(set(labels))
        self._unique_labels_count = len(labels)

        # Releases the memory for labels bit earlier.
        del labels

        self._line_ptr = 0
        self._example_ptr = 0
        self._feature_stack = None

        self._example_set = None
        self._location_set = None

    @staticmethod
    def _open_big_data_file(file_path):
        return open(file_path, "r", encoding="utf8")

    def _log(self, msg):
        if self._log_function is not None:
            self._log_function(msg)

    def _get_next_line(self):
        return self._file.readline().replace(BigDataFile.TEXT_FILE_LINE_SEPARATOR, "")

    def refresh_pointers(self):
        self._file.close()
        self._file = self._open_big_data_file(self._file.name)

        self._line_ptr = 0
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

    @staticmethod
    def _get_location_from_line(example : str):
        example_col_data = example.split(BigDataFile.TEXT_FILE_DATA_SEPARATOR)
        example_lat = example_col_data[consts.TEXT_FILE_COL_INDEX_GEO_LAT]
        example_long = example_col_data[consts.TEXT_FILE_COL_INDEX_GEO_LONG]
        return example_lat, example_long

    def get_next_example(self):
        if self._example_set is None or len(self._example_set) == 0:
            self._example_set = []

            for i in range(self._batch_size):
                line = self._get_next_line()
                if not line == "":
                    features_in_line = self._get_features_from_line(line)
                    label_for_line = self._get_label_from_line(line)

                    for feature_in_line in features_in_line:
                        example = {
                            BigDataFile.EXAMPLE_SET_KEY_FEATURE: feature_in_line,
                            BigDataFile.EXAMPLE_SET_KEY_LABEL: label_for_line
                        }

                        self._example_set.append(example)

                    self._line_ptr += 1
                else:
                    break

            if len(self._example_set) == 0:
                return None, None

        self._example_ptr += 1

        return_example = self._example_set.pop(0)
        return_example_feature = return_example[BigDataFile.EXAMPLE_SET_KEY_FEATURE]
        return_example_label = return_example[BigDataFile.EXAMPLE_SET_KEY_LABEL]
        return return_example_feature, return_example_label

    def get_next_location(self):
        if self._location_set is None or len(self._location_set) == 0:
            self._location_set = []

            for i in range(self._batch_size):
                line = self._get_next_line()
                if not line == "":
                    label_for_line = self._get_label_from_line(line)
                    lat_for_line, long_for_line = self._get_location_from_line(line)

                    location = {
                        BigDataFile.EXAMPLE_SET_KEY_LABEL: label_for_line,
                        BigDataFile.EXAMPLE_SET_KEY_LOCATION: (lat_for_line, long_for_line)
                    }

                    self._location_set.append(location)

                    self._line_ptr += 1
                else:
                    break

            if len(self._location_set) == 0:
                return None, None

        self._example_ptr += 1

        return_example = self._location_set.pop(0)
        return_example_label = return_example[BigDataFile.EXAMPLE_SET_KEY_LABEL]
        return_example_location = return_example[BigDataFile.EXAMPLE_SET_KEY_LOCATION]
        return return_example_label, return_example_location

    def get_file_line_count(self):
        return self._file_line_count

    def get_example_count(self):
        return self._example_count

    def get_unique_labels_count(self):
        return self._unique_labels_count

    def has_next_line(self):
        return self._line_ptr < self._file_line_count

    def has_next_example(self):
        return self._example_ptr < self._example_count

    def has_next_location(self):
        # Having a next line is same as having a unique location.
        return self.has_next_line()

    def get_current_example_ptr(self):
        return self._example_ptr

    def get_current_line_ptr(self):
        return self._line_ptr
