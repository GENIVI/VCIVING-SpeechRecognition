from emucorebrain.data.carriers.carrier import Carrier
from emucorebrain.io.mechanisms.ins_mechanism import InputMechanism


class InputMechanismCarrier(Carrier):

    CARRIER_TYPE = 0

    def __init__(self, data : InputMechanism):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, data : InputMechanism):
        self._data = data


