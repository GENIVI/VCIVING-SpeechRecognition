import multiprocessing
from threading import Timer
from emucorebrain.data.containers.settings import SettingsContainer
import commons.utils.queue as utils_queue
import commons.consts.queue as consts_queue
import time
import UniversalModelTrainerProcess.models.universal_trainer as trainer_universal
import UniversalModelTrainerProcess.config.trainers as config_trainers


def trigger_training(ivi_settings: SettingsContainer, queue_receive: multiprocessing.Queue, queue_send: multiprocessing.Queue):
    queue_send.put(consts_queue.PROCESS_FLAG_VALUE_SPAWNED)

    trainer_universal.init_trainers(ivi_settings)
    trainer_timer: Timer = None

    def exec_train_cycle():
        global trainer_timer

        trainer_universal.run_trainers()

        trainer_timer = Timer(config_trainers.TRAIN_INTERVAL, exec_train_cycle)
        trainer_timer.daemon = True
        trainer_timer.start()

    exec_train_cycle()

    process_destroy_flag: int = utils_queue.get_process_flag(queue_receive)
    while not process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_DESTROY:
        process_destroy_flag = utils_queue.get_process_flag(queue_receive)

        while process_destroy_flag == consts_queue.PROCESS_FLAG_VALUE_PAUSE:
            process_destroy_flag = utils_queue.get_process_flag(queue_receive)

            time.sleep(0.05)

        time.sleep(0.05)

    trainer_timer.cancel()
