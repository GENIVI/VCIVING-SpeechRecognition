# This is the "interface" class for all the input mechanisms
# Each an every input mechanism defined inside the mechanisms, should extend this class
import abc


class InputMechanism(abc.ABC):
    # This method is used to read data from the input mechanism.
    # It may or may not block the thread, really depends on what mechanism is used.
    # To find out whether the thread is blocked by this method, head over to respective mechanism.
    # To find out what type of return value is expected head over to the respective mechanism.
    @abc.abstractmethod
    def read_data(self):
        pass
