import pyaudio
import multiprocessing
import EavesdropProcess.consts.recordings as consts_recording
import EavesdropProcess.consts.queue as consts_queue
import EavesdropProcess.utils.queue as utils_queue
import EavesdropProcess.utils.recordings as utils_recordings
import time
import wave


def capture_and_save_audio(audio_file_time: int, save_folder_path: str, queue_receive: multiprocessing.Queue, queue_send: multiprocessing.Queue):
    queue_send.put(consts_queue.PROCESS_FLAG_VALUE_SPAWNED)

    pyaudio_obj = pyaudio.PyAudio()
    stream = pyaudio_obj.open(format=consts_recording.FORMAT, channels=consts_recording.CHANNELS,
                              rate=consts_recording.SAMPLING_RATE, input=True,
                              frames_per_buffer=consts_recording.CHUNK_SIZE)

    utils_recordings.convert_save_folder_to_eaves_folder(save_folder_path)

    process_destroy_flag: int = utils_queue.get_process_flag(queue_receive)
    while not process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_DESTROY:
        frames = []

        audio_file_start_time = time.time()
        for chunk_index in range(0, int((consts_recording.SAMPLING_RATE / consts_recording.CHUNK_SIZE) * audio_file_time)):
            process_destroy_flag = utils_queue.get_process_flag(queue_receive)
            if process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_DESTROY:
                break
            while process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_PAUSE:
                process_destroy_flag = utils_queue.get_process_flag(queue_receive)

            chunk_data = stream.read(consts_recording.CHUNK_SIZE)
            frames.append(chunk_data)

        audio_file_end_time = time.time()

        audio_file_path, transcription_file_path = utils_recordings.get_audio_file_names(eaves_folder_path=save_folder_path, start_time=audio_file_start_time, end_time=audio_file_end_time)

        # Writing the audio file
        audio_file = wave.open(audio_file_path, 'wb')
        audio_file.setnchannels(consts_recording.CHANNELS)
        audio_file.setsampwidth(pyaudio_obj.get_sample_size(consts_recording.FORMAT))
        audio_file.setframerate(consts_recording.SAMPLING_RATE)
        audio_file.writeframes(b''.join(frames))
        audio_file.close()

        # TODO: Write the transcription file too.

    stream.stop_stream()
    stream.close()
    pyaudio_obj.terminate()
