from threading import Thread

from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism, Grabber, GrabberController


# The Input Mechanism which requires data to be entered through the terminal.
# This will imitate the Microphone
class TerminalInputMechanism(InputMechanism):

    # Imitating the Microphone
    # This would ensure that the FindMapsExecutor would respond in the similar fashion as if Terminal is a Microphone.
    CONTAINER_KEY = "ins_mechanism_microphone"

    SENTENCE_TERMINATOR = "@end_kill"

    # Constructor
    # Used a Grabber and a Listening approach to suit with the FindMapsExecutor's requirements.
    def __init__(self):
        self._grabber_controller = GrabberController(self._get_default_grabbers(), notify_all=True)

        self._mechanism_alive = True
        self._listening_state = True

        self._last_input_text = None

        def _exec_listener():
            while self._mechanism_alive or self._listening_state:
                input_text = input()
                self._last_input_text = input_text
                # The second argument will be None to indicate that there is no exception, imitating the second argument passed in microphone Input Mechanism
                self._grabber_controller.notify_grabbers(input_text, None)

        listener_thread = Thread(target=_exec_listener)
        listener_thread.daemon = True
        listener_thread.start()

    # Used to check whether listening on this mechanism has been completely terminated.
    def is_mechanism_alive(self):
        return self._mechanism_alive

    # Internal/Private method used to obtain the default set of grabbers.
    def _get_default_grabbers(self):
        default_grabbers = []

        # Terminator Grabber to terminate the test program when SENTENCE_TERMINATOR sentence is detected
        def _exec_grabber_terminator(sentence, *args):
            if sentence == TerminalInputMechanism.SENTENCE_TERMINATOR:
                self.stop_listening(kill_permanently=True)
        default_grabbers.append(Grabber(on_exec=_exec_grabber_terminator))

        return default_grabbers

    def start_listening(self):
        self._mechanism_alive = True
        self._listening_state = True

    def stop_listening(self, kill_permanently=False):
        self._listening_state = False
        self._mechanism_alive = not kill_permanently

    def read_data(self):
        return self._last_input_text

    def get_grabber_controller(self):
        return self._grabber_controller
