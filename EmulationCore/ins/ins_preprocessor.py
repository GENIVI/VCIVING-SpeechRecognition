# This is the "interface" class for all the input pre-processors
# Each an every input pre-processor defined inside the preprocessor package, should extend this class.
import abc


class InputPreProcessor(abc.ABC):
    # This method is called whenever we need actually to perform data processing
    # This may be a time consuming process, head over to implementation to find out.
    # data should be a parameter of type string.
    @abc.abstractmethod
    def process_data(self, data):
        pass

