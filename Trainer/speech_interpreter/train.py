import consts
from speech_interpreter import file_reader
from emucorebrain.core.preprocessor import PreProcessor
from emucorebrain.core.trainer import Trainer
from emucorebrain.core.predictor import Predictor
import numpy as np

_train_data_filepath = consts.DATA_DIR_PATH + "/train_data.json"
_train_stem_ignore_filepath = consts.DATA_DIR_PATH + "/train_stem_ignore.txt"
_tasks_namespaces_folderpath = "D:/GENIVI/Projects/TaskExecutors"

_training_process_verbose = True
_training_hidden_neurons = 10
_training_gradient_descent_alpha = 1
_training_epochs = 1000
_training_batch_size = 3
_training_iterations = 2
_training_dropout = False
_training_dropout_percent = 0.5

nl_features, text_labels = file_reader.read_file_as_dataset(_train_data_filepath)
stem_blacklist_words = file_reader.read_file_as_ignore_list(_train_stem_ignore_filepath)

data_preproc = PreProcessor(nl_features, text_labels, stem_blacklist_words)
data_preproc.tokenize_and_stem()
data_preproc.convert_to_patterns()

# Checking for the validity of the implements Tasks
# Synapses and prediction threshold are not important here, just leave them at any arbitrary values.
empty_synapses = np.empty([1, 1])
arbitary_prediction_threshold = 0.2
validator_predictor = Predictor(trained_preprocessor=data_preproc, synapse0=empty_synapses, synapse1=empty_synapses, prediction_threshold=arbitary_prediction_threshold)
validator_predictor.run_validation_on_namespace_dir(_tasks_namespaces_folderpath)

trainer = Trainer(trained_preprocessor=data_preproc, train_verbose=_training_process_verbose, tasks_namespaces_folderpath=_tasks_namespaces_folderpath)
trainer.train(hidden_neurons=_training_hidden_neurons, alpha=_training_gradient_descent_alpha, epochs=_training_epochs, batch_size=_training_batch_size, iterations=_training_iterations, dropout=_training_dropout, dropout_percent=_training_dropout_percent)
trainer.save_model(consts.MODEL_SAVEFILE_PATH)
print("Training complete. Elapsed Time: " + str(trainer.get_training_time()))
