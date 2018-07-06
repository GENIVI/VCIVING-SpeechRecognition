from emucorebrain.data.carriers.carrier import Carrier


class StringCarrier(Carrier):

    CARRIER_TYPE = 2

    def __init__(self, data : str):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, data : str):
        self._data = data
