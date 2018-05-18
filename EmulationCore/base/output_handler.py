# This handles all the outputs and provides outputs as necessary

from outs.mechanisms.speaker import OutputSpeaker


def ivi_init_outputs():
    # Initialize the Speaker
    ivi_init_speaker()


##
#  SPEAKER
##
# Instance of OutputSpeaker
_speaker_output : OutputSpeaker = None


# General Methods
def ivi_run_outputs():
    _speaker_output.run_queued_data()
    # Other outputs called here to output their queued data


# Speaker Methods
def ivi_init_speaker():
    global _speaker_output

    _speaker_output = OutputSpeaker()

    # Update the speech rate to a more reasonable / understandable value when read.
    default_speech_rate = _speaker_output.get_speech_rate()
    new_speech_rate = default_speech_rate - 50
    _speaker_output.set_speech_rate(new_speech_rate)


def ivi_get_speaker() -> OutputSpeaker:
    return _speaker_output
# End of Speaker Methods
