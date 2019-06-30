from emucorebrain.data.abstracts.TaskExecutor import TaskExecutor
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism
from emucorebrain.data.carriers.string import StringCarrier
from emucorebrain.data.containers.settings import SettingsContainer
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier
import emucorebrain.keywords.task_executor as keywords_task_executor
from simpleaudio import PlayObject
from MusicPlayExecutor.LocalStorageForMusic import LocalStorageForMusic
from pydub import AudioSegment
import simpleaudio as audio_player


class MusicPlayExecutor(TaskExecutor):

    SETTING_LOCAL_SONGS_FOLDERPATH_KEY = "local_music_folderpath"

    OUTPUT_DATA_SONG_PLAYING = "A song is currently being played."

    # Use CD Quality Sampling Rate.
    PLAYER_SAMPLING_RATE = 44100
    # Since CD Quality has 16 bits per sample, we use 2 bytes per sample.
    PLAYER_BYTES_PER_SAMPLE = 2

    def __init__(self):
        self._current_audio : PlayObject = None

    def _play_audio_from_stream(self, audio_data, num_audio_channels, num_bytes_sample, sample_rate):
        self._current_audio = audio_player.play_buffer(audio_data, num_audio_channels, num_bytes_sample, sample_rate)

    def _play_audio_from_file(self, audio_file):
        with audio_file:
            sound = AudioSegment.from_file(audio_file)

            audio_data = sound.raw_data
            num_channels = sound.channels

            self._play_audio_from_stream(audio_data, num_channels, self.PLAYER_BYTES_PER_SAMPLE, self.PLAYER_SAMPLING_RATE)

    # Executes the negative run method of MusicPlayExecutor.
    def run_negative(self, args):
        pass

    # Executes the MusicPlayExecutor.
    # The main method executed when prediction is directed to this class.
    def run(self, args):
        data: StringCarrier = args[keywords_task_executor.ARG_SPEECH_TEXT_DATA]
        ivi_settings: SettingsContainer = args[keywords_task_executor.ARG_SETTINGS_CONTAINER]
        ivi_outs_mechanisms_carriers = args[keywords_task_executor.ARG_OUTS_MECHANISMS_CARRIERS]
        ivi_outs_mechanism_carrier_default: OutputMechanismCarrier = ivi_outs_mechanisms_carriers[keywords_task_executor.ARG_OUTS_MECHANISMS_MECHANISM_DEFAULT]
        ivi_outs_mechanism_default: OutputMechanism = ivi_outs_mechanism_carrier_default.get_data()

        if self._current_audio is None or not self._current_audio.is_playing():
            ivi_outs_mechanism_default.write_data("We are searching for the song. Please wait.", wait_until_completed=True)
            # We search for the song in the local storage
            local_songs_folderpath = ivi_settings.get_setting(MusicPlayExecutor.SETTING_LOCAL_SONGS_FOLDERPATH_KEY)
            local_songs = LocalStorageForMusic(local_songs_folderpath)
            song_file = local_songs.search(data.get_data())
            if song_file is not None:
                ivi_outs_mechanism_default.write_data("We found the song you've requested. Let's listen.", wait_until_completed=True)
                self._play_audio_from_file(song_file)
            else:
                ivi_outs_mechanism_default.write_data("We didn't find the song you've requested.", wait_until_completed=True)
                # TODO: Get permission from the user by asking to search internet for song because it is not found locally.
                # Then do it with the help of GoogleForMusic if permitted.
                pass
        else:
            self._current_audio.pause()
            ivi_outs_mechanism_default.write_data(MusicPlayExecutor.OUTPUT_DATA_SONG_PLAYING, wait_until_completed=True)
            self._current_audio.resume()
