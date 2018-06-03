# This is the "interface" class for all the output mechanisms
# Each an every output mechanism defined inside the mechanisms, should extend this class
import abc


class OutputMechanism(abc.ABC):
    # This method is used to output/write data to the output mechanism.
    # It may or may not block the thread, really depends on what mechanism is used.
    # To find out whether the thread is blocked by this method, head over to respective mechanism.
    # To find out what type of return value is expected head over to the respective mechanism.
    @abc.abstractmethod
    def write_data(self, data, wait_until_completed=False):
        pass

    # This method is called to output any queued data if there are any related to any implemented output mechanism
    # Head over to the implementation for more explanation.
    @abc.abstractmethod
    def run_queued_data(self):
        pass
