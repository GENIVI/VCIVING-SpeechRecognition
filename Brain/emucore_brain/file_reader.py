from emucore_brain.consts import consts
import os
import json


# Functions used in training
# This function reads the dataset file(training/test) as returns features and their labels as separate lists.
# Feature and its label should be delimited by a Tab Indent(\t) and each example must be delimited by newline(\n)
def read_file_as_dataset(file_path):
    file = open(file_path, "r")
    _, file_ext = os.path.splitext(file_path)
    file_ext = file_ext.replace(".", "")
    file_data = file.read()

    nl_features = []
    text_labels = []

    if file_ext == consts.extension_text:
        examples = file_data.split("\n")

        for example in examples:
            sep_example = example.split("\t")
            nl_features.append(sep_example[0])
            text_labels.append(sep_example[1])
    elif file_ext == consts.extension_json:
        examples = json.loads(file_data)

        for feature in examples:
            nl_features.append(feature)
            text_labels.append(examples[feature])

    return nl_features, text_labels


# This function reads the words to be ignored in stemming.
# The words must be delimited by newline(\n)
def read_file_as_ignore_list(file_path):
    file = open(file_path, "r")
    words = file.read().split("\n")

    return words

