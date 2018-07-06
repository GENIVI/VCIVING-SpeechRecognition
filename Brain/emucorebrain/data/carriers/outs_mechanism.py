from emucorebrain.data.carriers.carrier import Carrier
from emucorebrain.io.mechanisms.outs_mechanism import OutputMechanism


class OutputMechanismCarrier(Carrier):

    CARRIER_TYPE = 1

    def __init__(self, data : OutputMechanism):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, data : OutputMechanism):
        self._data = data
