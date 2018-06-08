# This is the "interface" class for all the tasks(basic functions that vehicle should perform)
# Each an every task should implement this.
import abc


class TaskExecutor(abc.ABC):

    VALID_TASK_EXECUTOR = True

    # The following method is directly called by the any other section of the program.
    # This is the function where one should implement the gist of the task to be performed.
    # No other methods defined by the implemented classes are called.
    @abc.abstractmethod
    def run(self):
        pass
