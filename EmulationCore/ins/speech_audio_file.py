from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, GrabberController

# This InputMechanism is used only by the terminal.
class InputSpeechAudioFile(InputMechanism):

    CONTAINER_KEY = "ins_mechanism_inputspeechaudiofile"

    def __init__(self, grabber_controller : GrabberController):
        self._grabber_controller = grabber_controller

    # This method is invalid for this InputMechanism, since processing is done on command request.
    def start_listening(self):
        pass

    # This method is invalid for this InputMechanism, since processing is done on command request.
    def stop_listening(self, raise_exception_if_stopped=True):
        pass

    # This method is invalid for this InputMechanism, since processing is done on command request.
    def read_data(self):
        pass

    def get_grabber_controller(self):
        return self._grabber_controller
