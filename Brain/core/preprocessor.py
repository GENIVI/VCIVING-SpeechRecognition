import consts
import nltk
from nltk.stem.lancaster import LancasterStemmer
import json
import os


class PreProcessor:

    # nl_features : Sentences
    # text_labels : Python namespaces for the file to be mapped for respective sentence
    def __init__(self, nl_features, text_labels, stem_blacklist_words):
        self._nl_features = nl_features
        self._text_labels = text_labels
        self._stem_blacklist_words = stem_blacklist_words

        self._word_list = []
        self._unique_labels_list = []
        self._nl_feature_label_map = []

        self._stemmer = LancasterStemmer()

        self._features = []
        self._labels = []

    def tokenize_and_stem(self):
        for i in range(0, len(self._nl_features)):
            nl_feature = self._nl_features[i]
            text_label = self._text_labels[i]

            tokenized_feature = nltk.word_tokenize(nl_feature)
            self._word_list.extend(tokenized_feature)
            self._nl_feature_label_map.append((tokenized_feature, text_label))

            if text_label not in self._unique_labels_list:
                self._unique_labels_list.append(text_label)

        self._word_list = [self._stemmer.stem(word.lower()) for word in self._word_list if word not in self._stem_blacklist_words]
        self._word_list = list(set(self._word_list))

        self._unique_labels_list = list(set(self._unique_labels_list))

    def convert_to_patterns(self):
        encoded_label_template = [0] * len(self._unique_labels_list)

        for example in self._nl_feature_label_map:
            words_in_example = example[0] # Get the word list of the example
            label_of_example = example[1] # Get the label of the example

            words_in_example = [self._stemmer.stem(word_in_example.lower()) for word_in_example in words_in_example] # Stem each word

            pattern_for_words = []
            for unique_word in self._word_list:
                if unique_word in words_in_example:
                    pattern_for_words.append(1)
                else:
                    pattern_for_words.append(0)

            encoded_label = list(encoded_label_template)
            encoded_label[self._unique_labels_list.index(label_of_example)] = 1

            self._features.append(pattern_for_words)
            self._labels.append(encoded_label)

    def get_text_labels(self):
        return self._text_labels

    def get_unique_text_labels(self):
        return list(set(self._text_labels))

    def get_processed_features_and_labels(self):
        return self._features, self._labels

    def get_processed_features(self):
        return self._features

    def get_processed_labels(self):
        return self._labels

    def get_feature_length(self):
        return len(self._word_list)

    def get_unique_label_count(self):
        return len(self._unique_labels_list)

    def get_unique_wordlist(self):
        return self._word_list

    def validate_tasks_directory(self, tasks_directory_path):
        if os.path.exists(tasks_directory_path):
            structure_definitions_filepath = tasks_directory_path + "/" + consts.TASKS_STRUCT_FILE_FILENAME

            if os.path.exists(structure_definitions_filepath):
                structure_definitions_file_data = open(structure_definitions_filepath).read()
                structure_definitions_file_data = json.loads(structure_definitions_file_data)

                if all(basic_prop in structure_definitions_file_data for basic_prop in consts.TASKS_STRUCT_FILE_BASIC_PROPERTY_KEYS):

                    all_executors = structure_definitions_file_data[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS]

                    for executor in all_executors:
                        executor_folder = executor[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_NAMESPACE]
                        executor_folder_path = tasks_directory_path + "/" + executor_folder

                        if os.path.exists(executor_folder_path):
                            executor_name = executor[consts.TASKS_STRUCT_FILE_PROP_EXECUTORS_CLASS]
                            executor_file_name = executor_name + ".py"
                            executor_file_path = executor_folder_path + "/" + executor_file_name

                            if not os.path.exists(executor_file_path):
                                return False, "Class File: " + executor_name + " cannot be found inside the Namespace Folder: " + executor_folder + "."
                        else:
                            return False, "Namespace folder: " + executor_folder + " not found."

                    return True, "Success"
                else:
                    return False, "One or more of the following required entries are not found in the " + consts.TASKS_STRUCT_FILE_FILENAME + ".\n" + consts.TASKS_STRUCT_FILE_PROP_DEP_DIRS + ", " + consts.TASKS_STRUCT_FILE_PROP_EXECUTORS
            else:
                return False, consts.TASKS_STRUCT_FILE_FILENAME + " does not exist inside " + tasks_directory_path +".\nPlease make sure the tasks executors folder path you've given contains valid TaskExecutors."
        else:
            return False, tasks_directory_path + " is an invalid directory."

    def get_sentence_patterns(self, sentence):
        tokenized_words = nltk.word_tokenize(sentence)
        stemmed_words = [self._stemmer.stem(tokenized_word.lower()) for tokenized_word in tokenized_words]

        patterns = [0] * len(self._word_list)
        for stemmed_word in stemmed_words:
            for index, trainingSet_word in enumerate(self._word_list):
                if stemmed_word == trainingSet_word:
                    patterns[index] = 1

        return patterns

    @staticmethod
    def get_sentence_patterns(sentence, word_list):
        tokenized_words = nltk.word_tokenize(sentence)
        stemmer = LancasterStemmer()
        stemmed_words = [stemmer.stem(tokenized_word.lower()) for tokenized_word in tokenized_words]

        patterns = [0] * len(word_list)
        for stemmed_word in stemmed_words:
            for index, trainingSet_word in enumerate(word_list):
                if stemmed_word == trainingSet_word:
                    patterns[index] = 1

        return patterns
