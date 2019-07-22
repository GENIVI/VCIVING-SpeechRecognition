import abc

# This is the "interface" class for all the processes.
# Each an every process defined, should extend this class.


# Processes are executed throughout the execution life cycle, regardless of user's input.
# Therefore must use lockers together with them.
class Process(abc.ABC):

    VALID_PROCESS = True

    # This method is used to start the process.
    # Usually called at initializing function.
    # Can be used in any form can initialize variables/can actually start the process or any other stuff.
    # Note: Never use threads to run the iteration method, run it over the exec_iter method to ensure that I/O doesn't get mixed up.
    @abc.abstractmethod
    def start_process(self, args):
        pass

    # This method is executed in each cycle of the main loop in main program.
    # The code that goes in depends on the process that is to be executed.
    @abc.abstractmethod
    def exec_iter(self):
        pass

    # Starts/Resumes a process that has been stopped/paused by pause_process method.
    # The code that goes in depends on the process that is to be executed.
    @abc.abstractmethod
    def resume_process(self):
        pass

    # This method is used to temporarily stop(pause) the process which can be started again using resume_process method
    # The code that goes in depends on the process that is to be executed.
    @abc.abstractmethod
    def pause_process(self):
        pass

    # This method is executed when the system wraps up or the process is needed to be stopped.
    # The code that goes in depends on the process.
    # Usually clean-up code goes in here.
    @abc.abstractmethod
    def destroy_process(self):
        pass
