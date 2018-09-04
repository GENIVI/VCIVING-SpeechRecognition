from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism

class StandardOutput(OutputMechanism):

    CONTAINER_KEY = "outs_mechanism_standardout"

    _STD_OUT_INDICATOR = "StandardOutput"

    def write_data(self, data, wait_until_completed=False):
        print(StandardOutput._STD_OUT_INDICATOR + ": " + data)

    def run_queued_data(self):
        pass

