import consts
import file_reader
from core.preprocessor import PreProcessor
from train.trainer import Trainer

_train_data_filepath = consts.data_dir_path + "/train_data.txt"
_train_stem_ignore_filepath = consts.data_dir_path + "/train_stem_ignore.txt"

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

trainer = Trainer(trained_preprocessor=data_preproc, train_verbose=_training_process_verbose)
trainer.train(hidden_neurons=_training_hidden_neurons, alpha=_training_gradient_descent_alpha, epochs=_training_epochs, batch_size=_training_batch_size, iterations=_training_iterations, dropout=_training_dropout, dropout_percent=_training_dropout_percent)
trainer.save_model(consts.model_savefile_path)
print("Training complete. Elapsed Time: " + str(trainer.get_training_time()))