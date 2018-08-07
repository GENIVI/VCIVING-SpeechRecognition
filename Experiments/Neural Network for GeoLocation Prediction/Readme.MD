# Experimental Approach for Using a Neural Network for Geo Location Prediction

Training and testing scripts for the Neural Network for identifying geo locations(latitude and longitudes) given the
location name.

Before continuing read more: https://at.projects.genivi.org/wiki/display/PROJ/Experimental+Approach%3A+Determining+Geo-Location+with+a+Neural+Network

## Requirements

- Python 3.6.5
- Pip 9.0.3

## Training the Model

- Training datasets can be obtained from: http://download.geonames.org/export/dump/
  - Any zip file containing a text file would work.
  - Once downloaded, the text file is the file to be treated as the training dataset, not the zip file.

- You need to install the dependencies for the project.
  - Open up a terminal in the directory of the cloned project.
  - Follow the following procedures to install everything required.
    1. Run the following command
      `pip install --upgrade -r requirements.txt`
    2. You need Tensorflow framework installed. Follow the [official guide here](https://www.tensorflow.org/install/) to get it installed.
       You will be offered the GPU or CPU version. Either of them would work.

- Change the following constants in train.py **only if needed**
  1. **_train_data_filepath**: Path to the training dataset text(.txt) file.
  2. **_train_model_save_folderpath**: Path to the directory in which the trained model is saved together with other serialized objects.
  3. **_training_feature_dict_size**: Size of the dictionary for the tokenizers. Increment in the size would enhance the security in the cost of training time and memory usage during training process.
  4. **_training_process_verbose**: Set True to switch on the verbose mode during the training process.
  5. **_training_epochs**: Number of epochs.
  6. **_training_batch_size**: Batch size of training data to be used.
  7. **_training_iterations**: Number of iterations per epoch.
  8. **_training_dropout_percent**: Percentage to be used in dropout layers of the model. Refer Keras Documentation.

- Run the following command to train the model.
    `python3 train.py`

- Note: The training process may take a while.

- Good Luck! ;)
