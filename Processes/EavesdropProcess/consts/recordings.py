import pyaudio


AUDIO_FILE_FORMAT = "wav"
TRANSCRIPTION_FILE_FORMAT = "transcription"

FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLING_RATE = 16000
CHUNK_SIZE = 1024
