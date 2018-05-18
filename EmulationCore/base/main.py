# This is the main thread of the program / base of the entire system
import base.input_handler as input_handler
import base.output_handler as output_handler
from threading import Thread

# Initializes all the outputs(mechanisms)
output_handler.ivi_init_outputs()
_output_speaker = output_handler.ivi_get_speaker()

# Initializes all the inputs(mechanisms)
input_handler.ivi_init_inputs(_output_speaker)

# Temporary content which is to be changed in the coming days
ivi_shutdown = False


def grab_user_input():
    global ivi_shutdown

    while not ivi_shutdown:
        user_input = input("Please type \"End\" to Finish or other Command to execute.\n")
        if user_input.lower() == "end":
            input_handler.ivi_stop_microphone()
            ivi_shutdown = True
        else:
            splitted_command = user_input.split(" ")
            if splitted_command[0].lower() == "say":
                to_utter = ""
                for splitted_item in splitted_command[1:]:
                    to_utter += " " + splitted_item

                _output_speaker.write_data(to_utter)


typed_input_thread = Thread(target=grab_user_input)
typed_input_thread.daemon = True
typed_input_thread.start()

while not ivi_shutdown:
    output_handler.ivi_run_outputs()
