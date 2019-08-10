from multiprocessing import Queue
import commons.consts.queue as consts_queue


def get_process_flag(queue: Queue):
    try:
        return queue.get(block=False)

    except:
        return consts_queue.PROCESS_FLAG_VALUE_RUN
