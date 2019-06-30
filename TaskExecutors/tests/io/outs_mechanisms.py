from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism


# The Output Mechanism which writes to the terminal.
class TerminalOutputMechanism(OutputMechanism):

    # Constructor
    def __init__(self):
        pass

    # Writes data into the terminal directly, without any queue
    def write_data(self, data, wait_until_completed=False):
        print(data)

    # No Queue Present in this Mechanism, therefore useless
    def run_queued_data(self):
        pass
