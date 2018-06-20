from TaskExecutor import TaskExecutor


class DriveExecutor(TaskExecutor):

    def run(self, data):
        print("From DriveExecutor: Executed")
