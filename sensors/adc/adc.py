# coding=utf-8
from abc import abstractmethod
import sys
import threading
from time import time
from sensors.counter import Counter
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

    def __init__(self, listener):
        super(ADC, self).__init__()
        self.daemon = True

        self.listener = listener

        # GPIO trigger interrupt pin
        self.TRIGGER = 25
        self.CLOCK = 11
        self.INPUT = 9
        self.EN0 = 8
        self.EN1 = 7

        # Set up SPI interface
        self.init_spi()

        # Set up GPIO interrupt
        self.init_gpio()

        # Set up quadrature encoder counter
        self.init_counter()

    def init_spi(self):
        log.info('Initialising SPI interface')
        # self.spi = spidev.SpiDev()
        #
        # # Open both channels
        # self.spi.open(0, 0)
        # self.spi.open(0, 1)
        #
        # # Set speed to 50MHz
        # self.spi.max_speed_hz = 50000000

    def init_gpio(self):
        log.info('Initialising GPIO trigger')
        GPIO.setmode(GPIO.BCM)
        # Set up falling edge detection on the trigger pin
        GPIO.setup(self.TRIGGER, GPIO.IN)

        GPIO.setup(self.CLOCK, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.INPUT, GPIO.IN)
        GPIO.setup(self.EN0, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.EN1, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

    def init_counter(self):
        self.counter = Counter()

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

        # Select channel 1
        GPIO.output(self.EN0, GPIO.LOW)

        data = list()
        for i in range(12):
            # Pull clock down
            GPIO.output(self.CLOCK, GPIO.LOW)
            # Read a bit
            bit = GPIO.input(self.INPUT)
            GPIO.output(self.CLOCK, GPIO.HIGH)
            data.append(bit)

        # Select channel 2
        GPIO.output(self.EN0, GPIO.HIGH)
        GPIO.output(self.EN1, GPIO.LOW)

        for i in range(12):
            # Pull clock down
            GPIO.output(self.CLOCK, GPIO.LOW)
            # Read a bit
            bit = GPIO.input(self.INPUT)
            GPIO.output(self.CLOCK, GPIO.HIGH)
            data.append(bit)

        GPIO.output(self.EN1, GPIO.HIGH)

        end = time()
        log.debug("Read event data in " + str((end - start) * 1000000) + "µs")
        print 'channel 1:', data[:12], '\t\tchannel 2:', data[12:]

        # Read the timestamp from the counter
        timestamp = self.counter.read()

        # Invoke the callback listener
        self.listener.on_event(data, timestamp)

    def cleanup(self):
        log.info('Cleaning up GPIO')
        GPIO.cleanup()


class EventListener(object):
    """
    Defines the methods that should be implemented by a class wishing to
    receive event updates from the ADC sensor.
    """

    @abstractmethod
    def on_event(self, event, timestamp):
        """
        Called when an incoming detection event occurs.
        """
        pass
