

# Functions used in training
# This function reads the dataset file(training/test) as returns features and their labels as separate lists.
# Feature and its label should be delimited by a Tab Indent(\t) and each example must be delimited by newline(\n)
def read_file_as_dataset(file_path):
    file = open(file_path, "r")
    examples = file.read().split("\n")

    nl_features = []
    text_labels = []
    for example in examples:
        sep_example = example.split("\t")
        nl_features.append(sep_example[0])
        text_labels.append(sep_example[1])

    return nl_features, text_labels


# This function reads the words to be ignored in stemming.
# The words must be delimited by newline(\n)
def read_file_as_ignore_list(file_path):
    file = open(file_path, "r")
    words = file.read().split("\n")
    return words

