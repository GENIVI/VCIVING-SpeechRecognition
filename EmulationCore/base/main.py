# This is the main thread of the program / base of the entire system
import base.input_handler as input_handler
import base.output_handler as output_handler
import base.process_handler as process_handler
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.containers.lockers import LockersContainer
import base.consts.consts as emucore_consts
from threading import Thread
import time
# Temporary content which is to be changed in the coming days
from emucorebrain.io.mechanisms.ins_mechanism import GrabberController
from ins.microphone import InputMicrophone

ivi_shutdown = False

# Initializes the Settings Container.
ivi_settings = SettingsContainer(emucore_consts.SETTINGS_FILEPATH)
# Initializes the Lockers Container
ivi_lockers = LockersContainer()

# Initializes all the outputs(mechanisms).
output_handler.ivi_init_outputs()
# Initializes all the inputs(mechanisms).
input_handler.ivi_init_inputs(ivi_settings, ivi_lockers)
# Initializes and starts all the processes.
process_handler.init_processes(ivi_settings, ivi_lockers)
process_handler.start_processes()
# Outputs the status via default output mechanism.
output_handler.output_via_mechanism(output_handler.default_output_mechanism, "Initialization successful. Waiting for Commands...", wait_until_completed=False, log=True)


def grab_text_input():
    global ivi_shutdown

    while not ivi_shutdown:
        user_input = input("Please type \"End\" to Finish or other Command to execute.\n")
        if user_input.lower() == "end":
            process_handler.destroy_processes()
            output_handler.output_via_mechanism(mechanism=output_handler.default_output_mechanism, data="Stopped the processes.", wait_until_completed=True, log=False)

            input_handler.ivi_stop_inputs(kill_permanently=True)
            output_handler.output_via_mechanism(mechanism=output_handler.default_output_mechanism, data="Stopped grabbing inputs.", wait_until_completed=True, log=False)

            ivi_shutdown = True
        else:
            splitted_command = user_input.split(" ")
            if splitted_command[0].lower() == "say":
                if not ivi_lockers.is_outputs_locked():
                    to_utter = ""
                    for splitted_item in splitted_command[1:]:
                        to_utter += " " + splitted_item

                    output_handler.output_via_mechanism(mechanism=output_handler.default_output_mechanism, data=to_utter, wait_until_completed=True, log=False)
            # "exec_def_im" = execute in default input mechanism
            elif splitted_command[0].lower() == "exec_def_im":
                to_proc = ""
                for splitted_item in splitted_command[1:]:
                    to_proc += " " + splitted_item

                # Notify the GrabberController of the Default InputMechanism.
                default_ins_mechanism_grabber_controller: GrabberController = input_handler.default_input_mechanism.get_grabber_controller()
                # Since the arguments differ from Mechanism to Mechanism, notify them in different ways with the proper
                # order of arguments.
                if input_handler.default_input_mechanism.CONTAINER_KEY == InputMicrophone.CONTAINER_KEY:
                    default_ins_mechanism_grabber_controller.notify_grabbers(to_proc, None)
                # For other mechanisms.


typed_input_thread = Thread(target=grab_text_input)
typed_input_thread.daemon = True
typed_input_thread.start()

while not ivi_shutdown:
    output_handler.ivi_run_outputs()
    time.sleep(0.05)
