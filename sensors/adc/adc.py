from abc import abstractmethod
import random
import threading
from time import sleep
from spidev import spidev
from util.logger import Logger

log = Logger(__name__).setup()


class ADC(threading.Thread):
    """
    Helper class used to read data from a single ADC chip in a separate thread.
    """
    def __init__(self, channel, listener):
        super(ADC, self).__init__()
        log.info('Initialising SPI interface')

        self.channel = channel
        self.listener = listener

        # Set up SPI interface
        self.spi = spidev.SpiDev()
        self.spi.open(0, channel)

    def run(self):
        """
        Read data continuously from the sensor.
        """
        while True:
            # Read/write some dummy data for now
            response = self.spi.xfer2([random.randint(0, 35),
                                       random.randint(0, 35)])
            # Invoke the callback listener
            self.listener.on_event(response)
            sleep(1)


class EventListener(object):
    """
    Defines the methods that should be implemented by a class wishing to
    receive event updates from the ADC sensor.
    """

    @abstractmethod
    def on_event(self, event):
        """
        Called when an incoming detection event occurs.
        """
        pass
