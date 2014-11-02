import RPi.GPIO as GPIO
import random
from util.logger import Logger

log = Logger(__name__).setup()


class Counter(object):
    """
    Quadrature encoder counter module.
    """
    def __init__(self):
        log.info('Initialising quadrature encoder counter')

        # D0 - D7
        self.data_pins = [4, 17, 27, 22, 5, 6, 13, 19]

        for pin in self.data_pins:
            log.info('Initialising pin %d' % pin)
            GPIO.setup(pin, GPIO.IN)

        self.EN1 = 23
        self.EN2 = 24
        self.SEL1 = 26
        self.SEL2 = 21

        # 4x count mode
        # GPIO.setup(self.EN1, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(self.EN2, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.SEL1, GPIO.OUT)
        GPIO.setup(self.SEL2, GPIO.OUT)

    def read(self):
        buf = list()

        # Read one byte at a time
        # buf.extend(self.read_byte(GPIO.LOW, GPIO.HIGH))
        # buf.extend(self.read_byte(GPIO.HIGH, GPIO.HIGH))
        # buf.extend(self.read_byte(GPIO.LOW, GPIO.LOW))
        buf.extend(self.read_byte(GPIO.HIGH, GPIO.LOW))

        # Return dummy data
        # return ''.join(str(random.randint(0, 1)) for _ in xrange(32))

        data = ''.join([str(bit) for bit in buf])
        print data
        return data

    def read_byte(self, SEL1, SEL2):
        GPIO.output(self.SEL1, SEL1)
        GPIO.output(self.SEL2, SEL2)

        buf = list()

        for pin in self.data_pins:
            buf.append(GPIO.input(pin))

        return buf

