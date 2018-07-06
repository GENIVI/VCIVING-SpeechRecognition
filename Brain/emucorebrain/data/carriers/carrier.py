import abc


class Carrier(abc.ABC):

    CARRIER_TYPE = -1

    @abc.abstractmethod
    def get_data(self):
        pass

    @abc.abstractmethod
    def set_data(self, data):
        pass
