from emucorebrain.data.models.lockers import LockerTypes


class LockersContainer:

    def __init__(self):
        self._lockers = {}
        self._locker_index = 0

    def get_lockers(self):
        return self._lockers

    def is_inputs_locked(self):
        for _, locker_type in self._lockers.items():
            if locker_type == LockerTypes.INPUT_MECHANISMS:
                return True

        return False

    def is_outputs_locked(self):
        for _, locker_type in self._lockers.items():
            if locker_type == LockerTypes.OUTPUT_MECHANISMS:
                return True

        return False

    def add_locker(self, locker_type):
        self._lockers[self._locker_index] = locker_type
        self._locker_index += 1
        return self._locker_index - 1

    def remove_locker(self, locker_index):
        del self._lockers[locker_index]
