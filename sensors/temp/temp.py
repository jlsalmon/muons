import random
from smbus import SMBus
from util.logger import Logger

log = Logger(__name__).setup()


class TemperatureSensor(object):
    def __init__(self):
        log.debug("Initialising temperature/humidity sensor")
        self.bus = SMBus(1)

        self.address = 0x40
        self.MEASURE_RELATIVE_TEMPERATURE = 0xE3
        self.MEASURE_RELATIVE_HUMIDITY = 0xE5

        self.READ_FIRMWARE_VERSION = '\x84\xb8'

    def read_firmware_version(self):

        self.bus.write_byte(self.address, 0x84)
        self.bus.write_byte(self.address, 0xB8)
        response = self.bus.read_byte(self.address)
        print 'firmware version:', response
        # response = self.bus.read_byte_data(self.address,
        #                                    0xB8)
        # print 'firmware version:', response
        return response

    def read_temperature(self):
        # Return dummy data for now
        # return 20. + random.random()

        response = self.bus.read_byte_data(self.address,
                                           self.MEASURE_RELATIVE_TEMPERATURE)
        print 'temperature:', response
        return response

    def read_humidity(self):
        # Return dummy data for now
        # return random.randint(40, 90)

        response = self.bus.read_byte_data(self.address,
                                           self.MEASURE_RELATIVE_HUMIDITY)
        print 'humidity:', response
        return response
