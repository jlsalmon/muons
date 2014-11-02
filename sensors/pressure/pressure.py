import random
from smbus import SMBus
from util.logger import Logger

log = Logger(__name__).setup()


class PressureSensor(object):
    def __init__(self):
        log.debug("Initialising pressure sensor")
        self.bus = SMBus(1)
        self.address = 0x60

    def read_pressure(self):
        # Return dummy data for now
        # return 100. + random.random()

        response = self.bus.read_byte_data(self.address,
                                           0x02)
        print 'data:', response
        return response
