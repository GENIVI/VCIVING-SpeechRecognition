import abc


# The abstract class to be implemented by each locator.
class Locator(abc.ABC):

    # Used to obtain the current locations as a tuple: latitude(double), longitude(double)
    @abc.abstractmethod
    def get_location(self):
        pass
