import datetime
import json
import time
import numpy as np
import keywords.model


class Trainer:

    def __init__(self, trained_preprocessor, train_verbose=False):
        self._trained_preprocessor = trained_preprocessor
        self._train_verbose = train_verbose

        self._training_start_time = None
        self._training_end_time = None

        self._list_features = self._trained_preprocessor.get_processed_features()
        self._list_labels = self._trained_preprocessor.get_processed_labels()

        self._labels = np.array(self._list_labels)

        self._ptr_next_batch_begin = 0

        self._synapse_0 = None
        self._synapse_1 = None

    def _log(self, msg):
        if self._train_verbose:
            print(msg)

    # Compute sigmoid Non Linearity
    @staticmethod
    def sigmoid(x):
        output = 1 / (1 + np.exp(-x))
        return output

    # Convert output of sigmoid function to its derivative
    @staticmethod
    def sigmoid_output_to_derivative(output):
        return output * (1 - output)

    def _next_feature_batch(self, batch_size):
        return_features_batch = []
        return_labels_batch = []

        next_batch_end = self._ptr_next_batch_begin + batch_size
        if next_batch_end > len(self._list_features):
            return_feature_batch = self._list_features[self._ptr_next_batch_begin:len(self._list_features)]
            return_labels_batch = self._list_labels[self._ptr_next_batch_begin:len(self._list_features)]

            count_from_beginning = next_batch_end - len(self._list_features)

            feature_batch_from_beginning = self._list_features[0:count_from_beginning]
            return_feature_batch.extend(feature_batch_from_beginning)

            labels_batch_from_beginning = self._list_labels[0:count_from_beginning]
            return_labels_batch.extend(labels_batch_from_beginning)

            self._ptr_next_batch_begin = count_from_beginning
        else:
            return_feature_batch = self._list_features[self._ptr_next_batch_begin:next_batch_end]
            return_labels_batch = self._list_labels[self._ptr_next_batch_begin:next_batch_end]

            # Checking whether all features are obtained
            if next_batch_end > (len(self._list_features) - 1):
                next_batch_end = 0

            self._ptr_next_batch_begin = next_batch_end

        return return_feature_batch, return_labels_batch

    def train(self, hidden_neurons=10, alpha=1, epochs=100, batch_size=None, iterations=100, dropout=False, dropout_percent=0.5):
        self._training_start_time = time.time()
        self._training_end_time = None

        self._ptr_next_batch_begin = 0

        self._synapse_0 = None
        self._synapse_1 = None

        all_classes = self._trained_preprocessor.get_unique_text_labels()

        if batch_size is None:
            batch_size = len(self._list_features)
            iterations = 1

        self._log("Training with %s neurons, alpha:%s, dropout:%s %s" % (hidden_neurons, str(alpha), dropout, dropout_percent if dropout else ''))
        self._log("Input matrix: " + str(len(self._list_features)) + "x" + str(len(self._list_features[0])) + "     Output matrix: 1x" + str(len(all_classes)))
        np.random.seed(1)

        last_mean_error = 1
        # randomly initialize our weights with mean 0
        synapse_0 = 2 * np.random.random((len(self._list_features[0]), hidden_neurons)) - 1
        synapse_1 = 2 * np.random.random((hidden_neurons, len(all_classes))) - 1

        prev_synapse_0_weight_update = np.zeros_like(synapse_0)
        prev_synapse_1_weight_update = np.zeros_like(synapse_1)

        synapse_0_direction_count = np.zeros_like(synapse_0)
        synapse_1_direction_count = np.zeros_like(synapse_1)

        stop_epochs = False
        for j in iter(range(epochs + 1)):
            if stop_epochs:
                break
            else:
                for i in range(iterations):
                    nnp_feature_batch, nnp_labels_batch = self._next_feature_batch(batch_size)
                    feature_batch = np.array(nnp_feature_batch)
                    labels_batch = np.array(nnp_labels_batch)
                    # Feed forward through layers 0, 1, and 2
                    layer_0 = feature_batch
                    layer_1 = self.sigmoid(np.dot(layer_0, synapse_0))

                    if dropout:
                        layer_1 *= np.random.binomial([np.ones((len(feature_batch), hidden_neurons))], 1 - dropout_percent)[0] * (1.0 / (1 - dropout_percent))

                    layer_2 = self.sigmoid(np.dot(layer_1, synapse_1))

                    # how much did we miss the target value?
                    layer_2_error = labels_batch - layer_2

                    # Check this
                    if (j % 10000) == 0 and j > 5000:
                        # if this 10k epoch's error is greater than the last epoch, break out
                        if np.mean(np.abs(layer_2_error)) < last_mean_error:
                            self._log("delta after " + str(j) + " iterations:" + str(np.mean(np.abs(layer_2_error))))
                            last_mean_error = np.mean(np.abs(layer_2_error))
                        else:
                            self._log("break: " + str(np.mean(np.abs(layer_2_error))) + ">" + last_mean_error)
                            stop_epochs = True
                            break

                    # in what direction is the target value?
                    # were we really sure? if so, don't change too much.
                    layer_2_delta = layer_2_error * self.sigmoid_output_to_derivative(layer_2)

                    # how much did each l1 value contribute to the l2 error (according to the weights)?
                    layer_1_error = layer_2_delta.dot(synapse_1.T)

                    # in what direction is the target l1?
                    # were we really sure? if so, don't change too much.
                    layer_1_delta = layer_1_error * self.sigmoid_output_to_derivative(layer_1)

                    synapse_1_weight_update = (layer_1.T.dot(layer_2_delta))
                    synapse_0_weight_update = (layer_0.T.dot(layer_1_delta))

                    if j > 0:
                        synapse_0_direction_count += np.abs(((synapse_0_weight_update > 0) + 0) - ((prev_synapse_0_weight_update > 0) + 0))
                        synapse_1_direction_count += np.abs(((synapse_1_weight_update > 0) + 0) - ((prev_synapse_1_weight_update > 0) + 0))

                    synapse_1 += alpha * synapse_1_weight_update
                    synapse_0 += alpha * synapse_0_weight_update

                    prev_synapse_0_weight_update = synapse_0_weight_update
                    prev_synapse_1_weight_update = synapse_1_weight_update

        self._synapse_0 = synapse_0
        self._synapse_1 = synapse_1

        self._training_end_time = time.time()

    def save_model(self, savefile_path):
        now = datetime.datetime.now()

        words = self._trained_preprocessor.get_unique_wordlist()
        unique_classes = self._trained_preprocessor.get_unique_text_labels()

        synapse = {keywords.model.save_file_synapse0: self._synapse_0.tolist(), keywords.model.save_file_synapse1: self._synapse_1.tolist(),
                   keywords.model.save_file_datetime: now.strftime("%Y-%m-%d %H:%M"),
                   keywords.model.save_file_words: words,
                   keywords.model.save_file_classes: unique_classes
                   }

        with open(savefile_path, 'w') as outfile:
            json.dump(synapse, outfile, indent=4, sort_keys=True)

    def get_training_time(self):
        return self._training_end_time - self._training_start_time
