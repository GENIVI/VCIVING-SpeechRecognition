# This is the "interface" class for all the tasks(basic functions that vehicle should perform)
# Each an every task should implement this.
import abc


class TaskExecutor(abc.ABC):

    VALID_TASK_EXECUTOR = True
    DEFAULT_NAME_RUN_METHOD = "run"

    # This method is used to handle any negative-type speech input to the same task type defined in run method.
    # This method is NOT the default method that would run if Task Executor is directly called.
    # Would have to explicitly call this method when defining training data.
    # args should be a dictionary of arguments that are taken inside set with the defined args inside the system.
    @abc.abstractmethod
    def run_negative(self, args):
        pass

    # The following method is directly called by the any other section of the program.
    # This is the function where one should implement the gist of the task to be performed.
    # No other methods defined by the implemented classes are called.
    # args should be a dictionary of arguments that are taken inside set with the defined args inside the system.
    @abc.abstractmethod
    def run(self, args):
        pass
