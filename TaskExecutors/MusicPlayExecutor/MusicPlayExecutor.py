from emucorebrain.data.abstracts.TaskExecutor import TaskExecutor
from MusicPlayExecutor.LocalStorageForMusic import LocalStorageForMusic
from pydub import AudioSegment
import simpleaudio as audio_player
import os


TMP_MUSIC_FOLDERPATH = "D:/Downloads/Music"


class MusicPlayExecutor(TaskExecutor):

    # Use CD Quality Sampling Rate.
    PLAYER_SAMPLING_RATE = 44100
    # Since CD Quality has 16 bits per sample, we use 2 bytes per sample.
    PLAYER_BYTES_PER_SAMPLE = 2

    def __init__(self):
        self._current_audio = None
        self._music_local_storage = LocalStorageForMusic(TMP_MUSIC_FOLDERPATH)

    def _play_audio_from_stream(self, audio_data, num_audio_channels, num_bytes_sample, sample_rate):
        self._current_audio = audio_player.play_buffer(audio_data, num_audio_channels, num_bytes_sample, sample_rate)
        # Temp code
        while self._current_audio.is_playing():
            pass

    def _play_audio_from_file(self, audio_file):
        with audio_file:
            sound = AudioSegment.from_file(audio_file)

            audio_data = sound.raw_data
            num_channels = sound.channels

            self._play_audio_from_stream(audio_data, num_channels, self.PLAYER_BYTES_PER_SAMPLE, self.PLAYER_SAMPLING_RATE)

    def run(self, args):
        data = args[0]
        # We search for the song in the local storage
        song_file = self._music_local_storage.search(os.listdir(TMP_MUSIC_FOLDERPATH), data)
        if song_file is not None:
            self._play_audio_from_file(song_file)
        else:
            # Get permission from the user by asking to search internet for song because it is not found locally.
            # Then do it with the help of GoogleForMusic if permitted.
            pass
