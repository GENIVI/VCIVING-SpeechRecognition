from emucorebrain.data.carriers.ins_mechanism import InputMechanismCarrier
from emucorebrain.data.carriers.outs_mechanism import OutputMechanismCarrier


def get_carries_by_mechanisms(carrier_type, dict_mechanisms):
    for mechanism_key in dict_mechanisms:
        if carrier_type == InputMechanismCarrier.CARRIER_TYPE:
            dict_mechanisms[mechanism_key] = InputMechanismCarrier(dict_mechanisms[mechanism_key])
        elif carrier_type == OutputMechanismCarrier.CARRIER_TYPE:
            dict_mechanisms[mechanism_key] = OutputMechanismCarrier(dict_mechanisms[mechanism_key])

    return dict_mechanisms
