import abc


# This is the "interface" class for all the input mechanisms
# Each an every input mechanism defined inside the mechanisms, should extend this class
class InputMechanism(abc.ABC):

    CONTAINER_KEY = None

    # This method is used to start listening on the device associated with the output mechanism
    # It would just be a simple function call to the input device which starts grabbing data from that respective
    # device.
    @abc.abstractmethod
    def start_listening(self):
        pass

    # This method is used to stop listening on the device associated with the output mechanism
    # It would just be a simple function call to the input device which stops grabbing data from that respective device.
    @abc.abstractmethod
    def stop_listening(self, raise_exception_if_stopped=True):
        pass

    # This method is used to read data from the input mechanism.
    # It may or may not block the thread, really depends on what mechanism is used.
    # To find out whether the thread is blocked by this method, head over to respective mechanism.
    # To find out what type of return value is expected head over to the respective mechanism.
    @abc.abstractmethod
    def read_data(self):
        pass

    # This method is used to return the GrabberController instance associated with the InputMechanism.
    # If GrabberControllers are not adopted in the implementation, this method may return None.
    # Otherwise, must return the associated GrabberController.
    @abc.abstractmethod
    def get_grabber_controller(self):
        pass


# Grabber is a wrapper around the function that is executed whenever an input is forwarded into it.
class Grabber:

    # Constructor for Grabber
    # on_exec: Function that should be executed when grabber receives data.
    def __init__(self, on_exec):
        self._on_exec = on_exec

    # Executes the function.
    # Accepts any number of positional or named arguments of any type which are directly passed into the function
    # executed.
    def exec(self, *args):
        self._on_exec(*args)


# GrabberController is a class that controls the Grabbers in a certain priority order.
class GrabberController:

    # The constant to identify the highest priority index.
    # Mostly used to debunk the confusion of index being least in numeric value over the highest priority.
    MAX_PRIORITY_INDEX = 0

    # Constructor for GrabberController
    # grabber_list: A python list which has it's items in the order of the priority.
    # notify_all: Set True to notify all the Grabbers in sequence of priority when data is received, False to notify
    # only the maximum priority Grabber.
    def __init__(self, grabber_list : list, notify_all=True):
        self._grabbers = {}
        for i, grabber in enumerate(grabber_list):
            self._grabbers[i] = grabber

        self._notify_all = notify_all

    # Adds a grabber into the grabber list prioritized by the given priority index.
    # If priority index is not followed up by the grabber, it is assumed as the least priority.
    # grabber: The new grabber to be added. An instance of Grabber class.
    # priority_index: The index of the priority that the grabber should be added into. Priority index is inversely
    # proportional to the priority. Higher the index, a lower priority is given. If left None, it is assumed that the
    # grabber is given the lowest priority available.
    def pop_in_grabber(self, grabber : Grabber, priority_index=None):
        # If priority index is None, assign it one more than the least priority of the current grabbers list,
        # i.e one more than the maximum index.
        if priority_index is None:
            priority_index = max(self._grabbers, key=int) + 1

        # Increases the lower priorities by 1 in order to add the new grabber at the specified priority index
        # In the case of the priority index being the least priority(highest index), re-assign the lower priorities
        # than the given priority a higher index, i.e. a more lower priority.
        lower_priority_grabber_indices = [key for key in self._grabbers if key >= priority_index]
        lower_priority_grabber_indices.sort(reverse=True)
        for lower_priority_index in lower_priority_grabber_indices:
            self._grabbers[lower_priority_index + 1] = self._grabbers[lower_priority_index]
            del self._grabbers[lower_priority_index]

        # Add the new grabber at the priority index.
        self._grabbers[priority_index] = grabber

    # Used to remove the Grabber at the given priority index.
    # priority_index: int representing the priority index at which the Grabber should be removed.
    # If left None, the Grabber with the least priority index(maximum index) is removed.
    def pop_out_grabber(self, priority_index=None):
        # If priority index is None, assign it the least priority of the current grabbers list, i.e the maximum index.
        if priority_index is None:
            priority_index = max(self._grabbers, key=int)

        # Removes the grabber at the specified priority index.
        if priority_index in self._grabbers:
            del self._grabbers[priority_index]
        else:
            raise Exception("There is no such priority index.")

        # Decreases the lower priorities by 1 as we have removed a grabber at a certain priority index.
        # In the case of the priority index being the least priority(highest index), re-assign the lower priorities
        # than the given priority a lower index, i.e. a more higher priority.
        lower_priority_grabber_indices = [key for key in self._grabbers if key > priority_index]
        lower_priority_grabber_indices.sort()
        for lower_priority_index in lower_priority_grabber_indices:
            self._grabbers[lower_priority_index - 1] = self._grabbers[lower_priority_index]
            del self._grabbers[lower_priority_index]

    # Used to get the Grabber at the given priority index.
    # priority_index: int representing the priority index at which the Grabber should be fetched.
    # If left None, the Grabber with the least priority index(maximum index) is returned.
    def get_out_grabber(self, priority_index=None):
        # If priority index is None, assign it the least priority of the current grabbers list, i.e the maximum index.
        if priority_index is None:
            priority_index = max(self._grabbers, key=int)

        return self._grabbers[priority_index]

    # Sets whether notify_grabbers method calls all the Grabbers' exec method in the order of their priority.
    # state: Set True to notify all the Grabbers in sequence of priority when data is received, False to notify
    # only the maximum priority Grabber.
    def set_notify_all(self, state : bool):
        self._notify_all = state

    # Executes the exec method of all the Grabbers in the order of maximum priority.
    # Pass any number of arguments to be passed directly to Grabber's exec method. Either positional or named.
    def notify_grabbers(self, *args):
        if self._notify_all:
            for grabber_index in self._grabbers:
                grabber : Grabber = self._grabbers[grabber_index]
                grabber.exec(*args)
        else:
            if GrabberController.MAX_PRIORITY_INDEX in self._grabbers:
                grabber : Grabber = self._grabbers[GrabberController.MAX_PRIORITY_INDEX]
                grabber.exec(*args)
            else:
                raise Exception("There is no single Grabber to be executed.")
