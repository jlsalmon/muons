from abc import abstractmethod
import random
import sys
import threading
from time import time
from spidev import spidev
from util.logger import Logger

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('Error importing RPi.GPIO!'
          ' This is probably because you need superuser privileges.'
          ' You can achieve this by using \'sudo\' to run your script')
    sys.exit(1)
except ImportError:
    print('Be sure to run this on a Raspberry Pi B+ ;)')
    print('Continuing anyway ...')

log = Logger(__name__).setup()


class ADC(threading.Thread):
    """
    Helper class used to read data from a single ADC chip in a separate thread.
    """
    def __init__(self, channel, listener):
        super(ADC, self).__init__()
        self.daemon = True

        self.channel = channel
        self.listener = listener

        # GPIO trigger interrupt pin
        self.TRIGGER = 22

        # Set up SPI interface
        self.init_spi()

        # Set up GPIO interrupt
        self.init_gpio()

    def init_spi(self):
        log.info('Initialising SPI interface')
        self.spi = spidev.SpiDev()
        self.spi.open(0, self.channel)

    def init_gpio(self):
        log.info('Initialising GPIO trigger')
        GPIO.setmode(GPIO.BOARD)
        # Set up falling edge detection on the trigger pin
        GPIO.setup(self.TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        """
        Called when the thread is started.
        """
        GPIO.add_event_detect(self.TRIGGER, GPIO.FALLING,
                              callback=self.on_trigger,
                              bouncetime=20)

    def on_trigger(self, channel):
        """
        Called when the trigger pin is pulled low. Immediately read data from
        the sensor.
        """
        start = time()
        # Read/write some dummy data for now
        response = self.spi.xfer2([random.randint(0, 35),
                                   random.randint(0, 35)])
        end = time()
        log.debug("Read event data in " + str((end - start) * 1000) + "ms")

        # Invoke the callback listener
        self.listener.on_event(response)

    def cleanup(self):
        log.info('Cleaning up GPIO')
        GPIO.cleanup()


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
